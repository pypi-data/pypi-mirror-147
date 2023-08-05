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
from .x_updatable import XUpdatable as XUpdatable_9a420ab0

class XUpdatable2(XUpdatable_9a420ab0):
    """
    This interface extends XUpdatable in order to provide more fine-tuned update modes.
    
    When performing a soft update, the implementor may decide not to update in certain cases, such as when the controller is locked. When performing a hard update, on the other hand, the implementor should perform update more aggressively even when the controller is locked.

    See Also:
        `API XUpdatable2 <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1util_1_1XUpdatable2.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.util.XUpdatable2']

    def updateHard(self) -> None:
        """
        Perform update, even when the controller is locked.
        """
    def updateSoft(self) -> None:
        """
        Perform update, but update may not always be performed especially when the controller is locked.
        """

