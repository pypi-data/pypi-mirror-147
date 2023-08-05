# coding: utf-8
#
# Copyright 2022 :Barry-Thomas-Paul: Moss
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Interface Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.util
from typing_extensions import Literal
from abc import ABC

class XLockable(ABC):
    """
    allows locking a component
    
    lock and unlock calls can be nested. However, they must be in pairs. As long as there has been one more call to lock than to unlock, the component is considered locked, which is reflected by isLocked() returning TRUE.

    See Also:
        `API XLockable <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1util_1_1XLockable.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.util.XLockable']

    def isLocked(self) -> bool:
        """
        determines whether the component is currently locked.
        """
    def lock(self) -> None:
        """
        locks the component
        """
    def unlock(self) -> None:
        """
        unlocks the component

        Raises:
            NotLockedException: ``NotLockedException``
        """

