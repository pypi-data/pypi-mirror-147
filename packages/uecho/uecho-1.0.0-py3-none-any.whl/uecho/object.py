# Copyright (C) 2021 Satoshi Konno. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
from typing import Optional, Union, Tuple, Dict, Any, List

from .property import Property
from .protocol.message import Message
from .protocol.subject import Subject
from .esv import ESV
from .util.bytes import Bytes


class ObjectRequestHandler(metaclass=abc.ABCMeta):
    """ObjectRequestHandler is an abstract handler class to handle to request messages to a device.
    """

    @abc.abstractmethod
    def property_read_requested(self, prop: Property) -> bool:
        """ Handles a read request message, and updates the propery data if needed.

        Args:
            prop (Property): The target property.

        Returns:
            bool: True if allowed the access, otherwise False.
        """
        pass

    @abc.abstractmethod
    def property_write_requested(self, prop: Property, data: bytes) -> bool:
        """ Handles a write request message, and updates the propery data by the specified data if allowed.

        Args:
            prop (Property): The target property.
            data (bytes): The update data.

        Returns:
            bool: True if allowed the update, otherwise False.
        """
        pass


class Object(object):
    """Object represents a object of ECHONET Lite, and it has child properties that includes the specification attributes and the dynamic data.
    """

    CODE_UNKNOWN = -1
    CODE_MIN = 0x000000
    CODE_MAX = 0xFFFFFF
    CODE_SIZE = 3
    CODE_UNKNOWN = CODE_MIN

    OPERATING_STATUS = 0x80
    MANUFACTURER_CODE = 0x8A
    ANNO_PROPERTY_MAP = 0x9D
    SET_PROPERTY_MAP = 0x9E
    GET_PROPERTY_MAP = 0x9F

    OPERATING_STATUS_ON = 0x30
    OPERATING_STATUS_OFF = 0x31
    OPERATING_STATUS_SIZE = 1
    MANUFACTURER_EVALUATION_CODE_MIN = 0xFFFFF0
    MANUFACTURER_EVALUATION_CODE_MAX = 0xFFFFFF
    MANUFACTURER_CODE_SIZE = 3
    PROPERTY_MAP_MAX_SIZE = 16
    ANNO_PROPERTY_MAP_MAX_SIZE = PROPERTY_MAP_MAX_SIZE + 1
    SET_PROPERTY_MAP_MAX_SIZE = PROPERTY_MAP_MAX_SIZE + 1
    GET_PROPERTY_MAP_MAX_SIZE = PROPERTY_MAP_MAX_SIZE + 1

    MANUFACTURER_UNKNOWN = MANUFACTURER_EVALUATION_CODE_MIN

    code: int
    name: str
    node: Optional[Any]
    __properties: Dict[int, Property]
    __request_handler: ObjectRequestHandler
    __msg_subject: Subject

    def __init__(self, code: Union[int, Tuple[int, int], Tuple[int, int, int], Any] = None):
        self.code = Object.CODE_UNKNOWN
        self.name = ""
        self.__properties = {}
        self.node = None
        self.__request_handler = None
        self.set_code(code)
        self.__msg_subject = Subject()

    def __del__(self):
        pass

    def set_code(self, code: Union[int, Tuple[int, int], Tuple[int, int, int], Any]) -> bool:
        """Sets the spcecified code as the object code.

        Args:
            code (Union[int, Tuple[int, int], Tuple[int, int, int], Any]): A code or tuple code.

        Returns:
            bool: True if the specified code is valid, otherwise False.
        """
        if code is None:
            return False
        if isinstance(code, Object):
            self.code = code.code
        elif type(code) is int:
            self.code = code
            return True
        elif type(code) is tuple:
            tuple_n = len(code)
            if tuple_n == 2:
                self.code = 0
                self.group_code = code[0]
                self.class_code = code[1]
                return True
            elif tuple_n == 3:
                self.code = 0
                self.group_code = code[0]
                self.class_code = code[1]
                self.instance_code = code[2]
                return True
        return False

    def is_code(self, code: Union[int, Tuple[int, int], Tuple[int, int, int], Any]) -> bool:
        """Checks whether the object has the specified code or belongs to the specified tuple code.

        Args:
            code (Union[int, Tuple[int, int], Tuple[int, int, int], Any]): A single code or tuple code.

        Returns:
            bool: True if the object belongs to the specified code, otherwise False.
        """
        if isinstance(code, Object):
            if self.code == code.code:
                return True
        elif type(code) is int:
            if self.code == code:
                return True
        elif type(code) is tuple:
            tuple_n = len(code)
            if tuple_n == 1:
                if self.group_code != code[0]:
                    return False
                return True
            if tuple_n == 2:
                if self.group_code != code[0]:
                    return False
                if self.class_code != code[1]:
                    return False
                return True
            elif tuple_n == 3:
                if self.group_code != code[0]:
                    return False
                if self.class_code != code[1]:
                    return False
                if self.instance_code != code[2]:
                    return False
                return True
        return False

    def is_group(self, code: int) -> bool:
        """Checks the object belongs to the specified group.

        Args:
            code (int): A group code.

        Returns:
            bool: True if the object belongs to the specified group, otherwise False.
        """
        return self.is_code((code,))

    def is_class(self, group_code: int, class_code: int) -> bool:
        """Checks the object belongs to the specified group and class.

        Args:
            group_code (int): A group code.
            class_code (int): A class code.

        Returns:
            bool: True if the object belongs to the specified group and class, otherwise False.
        """
        return self.is_code((group_code, class_code))

    @property
    def group_code(self):
        return ((self.code >> 16) & 0xFF)

    @group_code.setter
    def group_code(self, code: int):
        self.code |= ((code & 0xFF) << 16)

    @property
    def class_code(self):
        return ((self.code >> 8) & 0xFF)

    @class_code.setter
    def class_code(self, code: int):
        self.code |= ((code & 0xFF) << 8)

    @property
    def instance_code(self):
        return (self.code & 0xFF)

    @instance_code.setter
    def instance_code(self, code: int):
        self.code |= (code & 0xFF)

    @property
    def properties(self) -> List[Property]:
        return self.__properties.values()

    def add_property(self, prop: Property) -> bool:
        if not isinstance(prop, Property):
            return False
        self.__properties[prop.code] = prop
        prop.object = self
        return True

    def get_property(self, code: int) -> Optional[Property]:
        try:
            return self.__properties[code]
        except KeyError:
            return None

    def get_property_data(self, code: int) -> Optional[bytes]:
        try:
            return self.__properties[code].data
        except KeyError:
            return None

    def has_property(self, code: int) -> bool:
        prop = self.get_property(code)
        if not isinstance(prop, Property):
            return False
        return True

    def set_property_data(self, code: int, data: bytes) -> bool:
        prop = self.get_property(code)
        if prop is None:
            return False
        prop.data = data
        return True

    def set_property_string(self, code: int, data: str) -> bool:
        return self.set_property_data(code, data.encode('utf-8'))

    def set_property_integer(self, code: int, data: int, size: int) -> bool:
        return self.set_property_data(code, Bytes.from_int(data, size))

    def set_request_handler(self, listener: ObjectRequestHandler) -> bool:
        """ Sets a ObjectRequestHandler to handle read and write requests from other controllers and devices.

        Args:
            listener (ObjectRequestHandler): The listener that handles read and write requests from other controllers and devices.
        """
        self.__request_handler = listener
        return True

    def __create_message(self, esv: int, props: List[Tuple[int, bytes]]):
        msg = Message()
        msg.DEOJ = self.code
        msg.ESV = esv
        if not isinstance(props, list):
            return None
        for prop in props:
            if not isinstance(prop, tuple) or len(prop) != 2:
                return None
            if not isinstance(prop[0], int):
                return None
            if not isinstance(prop[1], bytes) and not isinstance(prop[1], bytearray):
                return None
            req = Property()
            req.code = prop[0]
            req.data = prop[1]
            msg.add_property(req)
        return msg

    def _set_object_properties(self, obj) -> bool:
        if not isinstance(obj, Object):
            return False
        self.name = obj.name
        for obj_prop in obj.properties:
            prop = obj_prop.copy()
            self.add_property(prop)
        return True

    def add_observer(self, observer) -> bool:
        """ Adds a message observer to the subject.

        Args:
            observer Observer: A message observer.

        Returns:
            bool: Returns True when the specified observer is added, Otherwise False.

        """
        return self.__msg_subject.add_observer(observer)

    def send_message(self, esv: int, props: List[Tuple[int, bytes]]) -> bool:
        """Sends a unicast message to the specified property asynchronously.

        Args:
            esv (int): A service type of ECHONET Lite.
            props (List[Tuple[int, bytes]]): List of a request property tuple (property code, property data).

        Returns:
            bool: True if successful, otherwise False.
        """
        msg = self.__create_message(esv, props)
        if msg is None:
            return False
        return self.node.controller.send_message(msg, self.node)

    def post_message(self, esv: int, props: List[Tuple[int, bytes]]) -> Optional[Any]:
        """Posts a unicast message to the specified property asynchronously.

        Args:
            esv (int): A service type of ECHONET Lite.
            props (List[Tuple[int, bytes]]): List of a request property tuple (property code, property data).

        Returns:
            Optional[Message]: The response message if successful receiving the response message, otherwise None.
        """
        msg = self.__create_message(esv, props)
        if msg is None:
            return None
        return self.node.controller.post_message(msg, self.node)

    def message_received(self, req_msg: Message) -> Optional[Message]:
        if not isinstance(req_msg, Message):
            return None

        self.__msg_subject.notify(req_msg)

        if not req_msg.is_request():
            return None

        if self.__request_handler is None:
            return None

        res_msg = Message()
        res_msg.TID = req_msg.TID
        res_msg.DEOJ = req_msg.SEOJ
        res_msg.SEOJ = req_msg.DEOJ

        accepted_request_cnt = 0

        if req_msg.is_write_read_request():
            for msg_prop in req_msg.set_properties:
                res_prop = Property(msg_prop.code)
                obj_prop = self.get_property(msg_prop.code)
                if obj_prop is not None:
                    if self.__request_handler.property_write_requested(obj_prop, msg_prop.data):
                        obj_prop.data = msg_prop.data
                        accepted_request_cnt += 1
                    else:
                        res_prop.data = msg_prop.data
                res_msg.add_set_property(res_prop)
            for msg_prop in req_msg.get_properties:
                res_prop = Property(msg_prop.code)
                obj_prop = self.get_property(msg_prop.code)
                if self.__request_handler.property_read_requested(obj_prop):
                    res_prop.data = obj_prop.data
                    accepted_request_cnt += 1
                res_msg.add_get_property(res_prop)
        else:
            for msg_prop in req_msg.properties:
                res_prop = Property(msg_prop.code)
                obj_prop = self.get_property(msg_prop.code)
                if obj_prop is not None:
                    if req_msg.is_read_request():
                        if self.__request_handler.property_read_requested(obj_prop):
                            res_prop.data = obj_prop.data
                            accepted_request_cnt += 1
                    elif req_msg.is_write_request():
                        if self.__request_handler.property_write_requested(obj_prop, msg_prop.data):
                            obj_prop.data = msg_prop.data
                            accepted_request_cnt += 1
                        else:
                            res_prop.data = msg_prop.data
                res_msg.add_property(res_prop)

        all_request_cnt = req_msg.OPC + req_msg.OPCSet + req_msg.OPCGet

        # 4.2.3.1 Property value write service (no response required) [0x60, 0x50]
        if req_msg.ESV == ESV.WRITE_REQUEST:
            if accepted_request_cnt == all_request_cnt:
                return None
            else:
                res_msg.ESV = ESV.WRITE_REQUEST_ERROR
                return res_msg

        # 4.2.3.2 Property value write service (response required) [0x61,0x71,0x51]
        if req_msg.ESV == ESV.WRITE_REQUEST_RESPONSE_REQUIRED:
            if accepted_request_cnt == all_request_cnt:
                res_msg.ESV = ESV.WRITE_RESPONSE
                return res_msg
            else:
                res_msg.ESV = ESV.WRITE_REQUEST_ERROR
                return res_msg

        # 4.2.3.3 Property value read service [0x62,0x72,0x52]
        if req_msg.ESV == ESV.READ_REQUEST:
            if accepted_request_cnt == all_request_cnt:
                res_msg.ESV = ESV.READ_RESPONSE
                return res_msg
            else:
                res_msg.ESV = ESV.READ_REQUEST_ERROR
                return res_msg

        # 4.2.3.4 Property value write & read service [0x6E,0x7E,0x5E]
        if req_msg.ESV == ESV.WRITE_READ_REQUEST:
            if accepted_request_cnt == all_request_cnt:
                res_msg.ESV = ESV.WRITE_READ_RESPONSE
                return res_msg
            else:
                res_msg.ESV = ESV.WRITE_READ_REQUEST_ERROR
                return res_msg

        # 4.2.3.5 Property value notification service [0x63,0x73,0x53]
        if req_msg.ESV == ESV.NOTIFICATION_REQUEST:
            if accepted_request_cnt == all_request_cnt:
                res_msg.ESV = ESV.NOTIFICATION
                return res_msg
            else:
                res_msg.ESV = ESV.NOTIFICATION_REQUEST_ERROR
                return res_msg

        # 4.2.3.6 Property value notification service (response required) [0x74, 0x7A]
        if req_msg.ESV == ESV.NOTIFICATION_RESPONSE_REQUIRED:
            if accepted_request_cnt == all_request_cnt:
                res_msg.ESV = ESV.NOTIFICATION_RESPONSE
                return res_msg

        return None

    def copy(self):
        obj = Object()
        obj.code = self.code
        obj.name = self.name
        for prop in self.__properties.values():
            obj.add_property(prop.copy())
        return obj
