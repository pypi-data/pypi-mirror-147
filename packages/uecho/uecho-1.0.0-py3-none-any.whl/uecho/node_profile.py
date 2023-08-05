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

import random

from typing import List
from .const import ECHONET_LITE_VERSION
from .profile import Profile
from .object import Object
from .std import Database
from .util.bytes import Bytes
from .property import Property
from .node import Node


class NodeProfile(Profile):
    CODE = 0x0EF001
    CLASS_CODE = 0xF0
    INSTANCE_GENERAL_CODE = 0x01
    INSTANCE_TRANSMISSION_ONLY_CODE = 0x02

    OPERATING_STATUS = Profile.OPERATING_STATUS
    VERSION_INFORMATION = 0x82
    IDENTIFICATION_NUMBER = 0x83
    FAULT_CONTENT = 0x89
    UNIQUE_IDENTIFIER_DATA = 0xBF
    NUMBER_OF_SELF_NODE_INSTANCES = 0xD3
    NUMBER_OF_SELF_NODE_CLASSES = 0xD4
    INSTANCE_LIST_NOTIFICATION = 0xD5
    SELF_NODE_INSTANCE_LIST_S = 0xD6
    SELF_NODE_CLASS_LIST_S = 0xD7

    OPERATING_STATUS_SIZE = 1
    VERSION_INFORMATION_SIZE = 4
    IDENTIFICATION_MANUFACTURER_CODE_SIZE = 3
    IDENTIFICATION_UNIQUE_ID_SIZE = 13
    IDENTIFICATION_NUMBER_SIZE = 1 + IDENTIFICATION_MANUFACTURER_CODE_SIZE + IDENTIFICATION_UNIQUE_ID_SIZE
    FAULT_CONTENT_SIZE = 2
    UNIQUE_IDENTIFIER_DATA_SIZE = 2
    NUMBER_OF_SELF_NODE_INSTANCES_SIZE = 3
    NUMBER_OF_SELF_NODE_CLASSES_SIZE = 2
    SELF_NODE_INSTANCE_LIST_S_MAX = 0xFF
    SELF_NODE_CLASS_LIST_S_MAX = 0xFF
    INSTANCE_LIST_NOTIFICATION_MAX = SELF_NODE_INSTANCE_LIST_S_MAX

    OPERATING_STATUS_ON = Profile.OPERATING_STATUS_ON
    OPERATING_STATUS_OFF = Profile.OPERATING_STATUS_OFF
    BOOTING = 0x30
    NOT_BOOTING = 0x31
    LOWER_COMMUNICATION_LAYER_PROTOCOL_TYPE = 0xFE

    def __init__(self):
        super().__init__(NodeProfile.CODE)
        std_obj = Database().get_object(NodeProfile.CODE)
        if isinstance(std_obj, Object):
            self._set_object_properties(std_obj)
        self.set_request_handler(self)
        self.__update_initial_properties()
        self.update_class_instance_properties([self])

    def __update_initial_properties(self) -> bool:
        self.set_property_integer(NodeProfile.OPERATING_STATUS, NodeProfile.BOOTING, NodeProfile.OPERATING_STATUS_SIZE)
        self.set_property_integer(NodeProfile.VERSION_INFORMATION, ECHONET_LITE_VERSION, NodeProfile.VERSION_INFORMATION_SIZE)
        self.__update_id_number()
        self.__update_unique_id()
        return True

    def __update_id_number(self) -> bool:
        id_bytes = bytearray([NodeProfile.LOWER_COMMUNICATION_LAYER_PROTOCOL_TYPE, 0x00, 0x00, 0x00])
        for _ in range(NodeProfile.IDENTIFICATION_UNIQUE_ID_SIZE):
            id_bytes.append(random.randint(1, 0xFF))
        return self.set_property_data(NodeProfile.IDENTIFICATION_NUMBER, id_bytes)

    def __update_unique_id(self) -> bool:
        id_bytes = bytearray()
        id_bytes.append(random.randint(1, 0xFF) & 0xC0)
        id_bytes.append(random.randint(1, 0xFF))
        return self.set_property_data(NodeProfile.UNIQUE_IDENTIFIER_DATA, id_bytes)

    def __is_node_profile_object(self, obj) -> bool:
        if obj.code == NodeProfile.CODE:
            return True
        if obj.code == NodeProfileReadOnly.CODE:
            return True
        return False

    def __update_instance_properties(self, objs: List[Object]) -> bool:
        instance_cnt = 0
        instance_list = bytearray()
        for obj in objs:
            if self.__is_node_profile_object(obj):
                continue
            instance_cnt += 1
            instance_list.extend(Bytes.from_int(obj.code, 3))

        if not self.set_property_data(NodeProfile.NUMBER_OF_SELF_NODE_INSTANCES, Bytes.from_int(instance_cnt, NodeProfile.NUMBER_OF_SELF_NODE_INSTANCES_SIZE)):
            return False

        instance_list_bytes = bytearray(Bytes.from_int(instance_cnt, 1))
        instance_list_bytes.extend(instance_list)
        if not self.set_property_data(NodeProfile.INSTANCE_LIST_NOTIFICATION, instance_list_bytes):
            return False
        if not self.set_property_data(NodeProfile.SELF_NODE_INSTANCE_LIST_S, instance_list_bytes):
            return False

        return True

    def __update_class_properties(self, objs: List[Object]) -> bool:
        class_cnt = 0
        class_list = bytearray()
        for obj in objs:
            class_cnt += 1
            if self.__is_node_profile_object(obj):
                continue
            has_same_class = False
            for n in range(0, len(class_list), 2):
                if class_list[n] == obj.group_code and class_list[n + 1] == obj.class_code:
                    has_same_class = True
                    break
            if has_same_class:
                continue
            class_list.extend(bytes([obj.group_code, obj.class_code]))

        if not self.set_property_data(NodeProfile.NUMBER_OF_SELF_NODE_CLASSES, Bytes.from_int(class_cnt, NodeProfile.NUMBER_OF_SELF_NODE_CLASSES_SIZE)):
            return False

        class_list_bytes = bytearray(Bytes.from_int(class_cnt, 1))
        class_list_bytes.extend(class_list)
        if not self.set_property_data(NodeProfile.SELF_NODE_CLASS_LIST_S, class_list_bytes):
            return False

        return True

    def __set_property_map_property(self, code: int, prop_map: List[int]) -> bool:
        map_bytes = bytearray(bytes([len(prop_map)]))
        for prop_code in prop_map:
            map_bytes.extend(bytes([prop_code]))
        if not self.set_property_data(code, map_bytes):
            return False
        return True

    def __update_property_map_properties(self, objs: List[Object]) -> bool:
        anno_list = []
        get_list = []
        set_list = []
        for obj in objs:
            for prop in obj.properties:
                if prop.is_announce_required():
                    anno_list.append(prop.code)
                if prop.is_read_enabled():
                    get_list.append(prop.code)
                if prop.is_write_enabled():
                    set_list.append(prop.code)
        anno_map = list(set(anno_list))
        get_map = list(set(get_list))
        set_map = list(set(set_list))
        if not self.__set_property_map_property(NodeProfile.ANNO_PROPERTY_MAP, anno_map):
            return False
        if not self.__set_property_map_property(NodeProfile.GET_PROPERTY_MAP, get_map):
            return False
        if not self.__set_property_map_property(NodeProfile.SET_PROPERTY_MAP, set_map):
            return False
        return True

    def update_class_instance_properties(self, objs: List[Object]) -> bool:
        if not self.__update_instance_properties(objs):
            return False
        if not self.__update_class_properties(objs):
            return False
        if not self.__update_property_map_properties([self]):
            return False
        return True

    def property_read_requested(self, prop: Property) -> bool:
        if isinstance(self.node, Node):
            self.update_class_instance_properties(self.node.objects)
        return True

    def property_write_requested(self, prop: Property, data: bytes) -> bool:
        return False


class NodeProfileReadOnly(NodeProfile):
    CODE = 0x0EF002

    def __init__(self):
        super().__init__()
        self.set_code(NodeProfileReadOnly.CODE)
