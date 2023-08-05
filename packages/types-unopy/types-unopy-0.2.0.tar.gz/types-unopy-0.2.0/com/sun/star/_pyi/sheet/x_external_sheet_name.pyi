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
# Namespace: com.sun.star.sheet
from typing_extensions import Literal
from ..uno.x_interface import XInterface as XInterface_8f010a43

class XExternalSheetName(XInterface_8f010a43):
    """
    provides a method to set an external name at the sheet.
    
    An external reference in a cell formula is implemented using a hidden sheet which is linked to the sheet in the external document. The name of the hidden sheet is composed of the URL of the external document and the external sheet name.
    
    **since**
    
        OOo 3.0

    See Also:
        `API XExternalSheetName <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sheet_1_1XExternalSheetName.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sheet.XExternalSheetName']

    def setExternalName(self, aUrl: str, aSheetName: str) -> None:
        """
        sets an external name at the sheet.
        
        This method allows to compose the sheet name from the URL of the external document and the name of the external sheet.

        Raises:
            com.sun.star.container.ElementExistException: ``ElementExistException``
        """

