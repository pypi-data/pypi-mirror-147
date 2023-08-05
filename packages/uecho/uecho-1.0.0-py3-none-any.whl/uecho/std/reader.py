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

from typing import Optional, Union, Tuple, Any
from ..object import Object
from ..manufacturer import Manufacture as ManufactureBase
from ..property import Property as PropertyBase
from ..util import Bytes

class Manufacture(ManufactureBase):

    def __init__(self, code: int, name: str):
        super().__init__()
        self.name = name
        self.code = code

class Object(Object):

    def __init__(self, name: str = "", grp_code: int = 0, cls_code: int = 0):
        super().__init__()
        self.name = name
        self.group_code = grp_code
        self.class_code = cls_code

class Property(PropertyBase):
    typ: str

    def __init__(self, code: int, name: str, typ: str, size: int, get: Any, set: Any, anno: Any):
        super().__init__()
        self.code = code
        self.name = name
        self.typ = typ
        self.size = size
        self.set_attribute(PropertyBase.GET, self.__to_attribute(get))
        self.set_attribute(PropertyBase.SET, self.__to_attribute(set))
        self.set_attribute(PropertyBase.ANNO, self.__to_attribute(anno))

    def __to_attribute(self, val: Any) -> int:
        attr = Property.PROHIBITED
        if isinstance(val, int):
            attr = val
        if isinstance(val, str):
            if val.lower() == "mandatory" or val.lower() == "required":
                attr = Property.REQUIRED
            elif val.lower() == "optional":
                attr = Property.OPTIONAL
        return attr