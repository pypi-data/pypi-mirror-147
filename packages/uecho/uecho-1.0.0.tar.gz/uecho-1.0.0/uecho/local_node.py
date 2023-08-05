# Copyright (C) 2021 Satoshi Konno. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

from typing import List
from .frame.manager import Manager
from .node import Node
from .node_profile import NodeProfile
from .protocol.message import Message as ProtocolMessage
from .message import Message
from .object import Object
from .option import IGNORE_SELF_MESSAGE


class LocalNode(Node):

    __manager: Manager
    __node_profile_obj: NodeProfile
    __options: int

    def __init__(self):
        super().__init__()
        self.__manager = Manager()
        self.__node_profile_obj = NodeProfile()
        self.__options = IGNORE_SELF_MESSAGE
        self.add_object(self.__node_profile_obj)

    def __del__(self):
        self.stop()

    def add_object(self, obj: Object) -> bool:
        if not super().add_object(obj):
            return False
        return self.__node_profile_obj.update_class_instance_properties(self.objects)

    def add_observer(self, observer):
        return self.__manager.add_observer(observer)

    def announce_message(self, msg: Message) -> bool:
        return self.__manager.announce_message(msg)

    def send_message(self, msg: Message, addr) -> bool:
        return self.__manager.send_message(msg, addr)

    def set_enabled(self, opt: int, v: bool) -> bool:
        if v:
            self.__options |= opt
        else:
            self.__options &= ~opt
        return True

    def is_enabled(self, opt: int) -> bool:
        if (self.__options & opt) == 0:
            return False
        return True

    def start(self, ifaddrs: List[str] = []) -> bool:
        if not self.__manager.start():
            return False
        self.set_address((self.__manager.ifaddr, self.__manager.port))
        self.__manager.add_observer(self)
        return True

    def stop(self) -> bool:
        return self.__manager.stop()

    def _is_self_message(self, proto_msg: ProtocolMessage):
        if proto_msg.from_addr != self.address:
            return False

    def message_received(self, proto_msg: ProtocolMessage):
        if self.is_enabled(IGNORE_SELF_MESSAGE):
            if self._is_self_message(proto_msg):
                return

        req_msg = Message(proto_msg)

        # 4.2.1 Basic Sequences for Service Content
        dest_obj = self.get_object(req_msg.DEOJ)
        if dest_obj is None:
            return

        res_msg = dest_obj.message_received(req_msg)

        # (A) Basic sequence for receiving a request (no response required)
        if res_msg is None:
            return

        if res_msg.is_notification():
            # (C) Basic sequence for processing a notification request
            self.announce_message(res_msg)
        else:
            # (B) Basic sequence for receiving a request (response required)
            self.send_message(res_msg, req_msg.from_addr)
