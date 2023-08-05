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

import socket
import threading
from typing import Any, Optional, List

from ..protocol.message import Message
from .observer import Observer


class Subject():
    observers: List[Observer]

    def __init__(self):
        self.observers = []

    def add_observer(self, observer) -> bool:
        """ Adds a message observer to the subject.

        Args:
            observer Observer: A message observer.

        Returns:
            bool: Returns True when the specified observer is added, Otherwise False.

        """
        if object is None:
            return False
        for added_observer in self.observers:
            if observer == added_observer:
                return True
        self.observers.append(observer)
        return True

    def notify(self, msg: Message):
        """Notifies the specified message to the added observers.

        Args:
            msg (Message): A notify message 
        """
        for observer in self.observers:
            observer.message_received(msg)
