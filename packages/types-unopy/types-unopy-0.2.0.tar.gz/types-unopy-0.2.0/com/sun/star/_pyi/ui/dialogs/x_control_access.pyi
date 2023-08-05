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
# Namespace: com.sun.star.ui.dialogs
from typing_extensions import Literal
from ...uno.x_interface import XInterface as XInterface_8f010a43

class XControlAccess(XInterface_8f010a43):
    """
    Generic control access interface.
    
    Use this interface to access user interface controls supported by the implementing service. The supported controls, control properties and the appropriate values are documented in the description of the implementing service.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XControlAccess <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1ui_1_1dialogs_1_1XControlAccess.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.ui.dialogs.XControlAccess']

    def getControlProperty(self, aControlName: str, aControlProperty: str) -> object:
        """
        Query for a control property.

        Raises:
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    def setControlProperty(self, aControlName: str, aControlProperty: str, aValue: object) -> None:
        """
        Change a control property.

        Raises:
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """

