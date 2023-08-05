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
# Namespace: com.sun.star.text
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..container.x_enumeration_access import XEnumerationAccess as XEnumerationAccess_4bac0ffc
    from ..container.x_name_access import XNameAccess as XNameAccess_e2ab0cf6

class XTextFieldsSupplier(XInterface_8f010a43):
    """
    makes it possible to access the text fields used in this context (e.g.
    
    this document).

    See Also:
        `API XTextFieldsSupplier <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XTextFieldsSupplier.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.text.XTextFieldsSupplier']

    def getTextFieldMasters(self) -> 'XNameAccess_e2ab0cf6':
        """
        """
    def getTextFields(self) -> 'XEnumerationAccess_4bac0ffc':
        """
        """

