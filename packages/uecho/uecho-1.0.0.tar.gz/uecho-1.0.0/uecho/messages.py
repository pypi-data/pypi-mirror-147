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

from .message import Message
from .esv import ESV
from .node_profile import NodeProfile
from .property import Property


class SearchMessage(Message):

    def __init__(self):
        super().__init__()
        self.ESV = ESV.READ_REQUEST
        self.SEOJ = NodeProfile.CODE
        self.DEOJ = NodeProfile.CODE
        prop = Property()
        prop.code = NodeProfile.SELF_NODE_INSTANCE_LIST_S
        prop.data = bytearray()
        self.add_property(prop)


class ReadRequest(Message):

    def __init__(self, DEOJ: int):
        super().__init__()
        self.ESV = ESV.READ_REQUEST
        self.SEOJ = NodeProfile.CODE
        self.DEOJ = DEOJ


class WriteRequest(Message):

    def __init__(self, DEOJ: int):
        super().__init__()
        self.ESV = ESV.WRITE_REQUEST
        self.SEOJ = NodeProfile.CODE
        self.DEOJ = DEOJ


class WriteResponseRequiredRequest(Message):

    def __init__(self, DEOJ: int):
        super().__init__()
        self.ESV = ESV.WRITE_REQUEST_RESPONSE_REQUIRED
        self.SEOJ = NodeProfile.CODE
        self.DEOJ = DEOJ


class WriteReadRequest(Message):

    def __init__(self, DEOJ: int):
        super().__init__()
        self.ESV = ESV.WRITE_READ_REQUEST
        self.SEOJ = NodeProfile.CODE
        self.DEOJ = DEOJ
