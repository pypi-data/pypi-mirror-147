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

from typing import Tuple, Union, Optional

from .protocol.message import Message as ProtocolMessage
from .property import Property
from .node_profile import NodeProfile
from .esv import ESV


class Message(ProtocolMessage):

    def __init__(self, msg: ProtocolMessage = None):
        super().__init__()
        if isinstance(msg, ProtocolMessage):
            self.parse_bytes(msg.to_bytes())
            self.from_addr = msg.from_addr
            self.to_addr = msg.to_addr

    def is_node_profile_message(self):
        if self.ESV != ESV.NOTIFICATION and self.ESV != ESV.READ_RESPONSE:
            return False
        if self.DEOJ != NodeProfile.CODE and self.DEOJ != NodeProfile.CODE_READ_ONLY:
            return False
        return True

    def __to_property(self, prop: Union[Property, Tuple[int, bytes], int]) -> Optional[Property]:
        new_prop = None
        if isinstance(prop, Property):
            new_prop = prop
        elif isinstance(prop, int):
            new_prop = Property()
            new_prop.code = prop
        elif isinstance(prop, tuple):
            if len(prop) != 2:
                return False
            new_prop = Property()
            new_prop.code = prop[0]
            new_prop.data = prop[1]
        return new_prop

    def add_property(self, prop: Union[Property, Tuple[int, bytes], int]) -> bool:
        """Adds the specified property to the message.

        Args:
            prop (Union[Property, Tuple[int, bytes]]): The new property. The property code is required, but the property bytes are optional.

        Returns:
            bool: Returns True when the specified property is added, Otherwise False.
        """
        new_prop = self.__to_property(prop)
        if new_prop is None:
            return False
        return super().add_property(new_prop)

    def add_set_property(self, prop: Union[Property, Tuple[int, bytes], int]) -> bool:
        """Adds the specified property to the message.

        Args:
            prop (Union[Property, Tuple[int, bytes]]): The new property. The property code is required, but the property bytes are optional.

        Returns:
            bool: Returns True when the specified property is added, Otherwise False.
        """
        new_prop = self.__to_property(prop)
        if new_prop is None:
            return False
        return super().add_set_property(new_prop)

    def add_get_property(self, prop: Union[Property, Tuple[int, bytes], int]) -> bool:
        """Adds the specified property to the message.

        Args:
            prop (Union[Property, Tuple[int, bytes]]): The new property. The property code is required, but the property bytes are optional.

        Returns:
            bool: Returns True when the specified property is added, Otherwise False.
        """
        new_prop = self.__to_property(prop)
        if new_prop is None:
            return False
        return super().add_get_property(new_prop)
