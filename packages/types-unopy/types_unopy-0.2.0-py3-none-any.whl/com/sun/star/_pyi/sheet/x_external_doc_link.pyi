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
import typing
from ..container.x_enumeration_access import XEnumerationAccess as XEnumerationAccess_4bac0ffc
from ..container.x_index_access import XIndexAccess as XIndexAccess_f0910d6d
from ..container.x_name_access import XNameAccess as XNameAccess_e2ab0cf6
if typing.TYPE_CHECKING:
    from .x_external_sheet_cache import XExternalSheetCache as XExternalSheetCache_1a420e89

class XExternalDocLink(XEnumerationAccess_4bac0ffc, XIndexAccess_f0910d6d, XNameAccess_e2ab0cf6):
    """
    Primary interface for the com.sun.star.sheet.ExternalDocLink service.
    
    **since**
    
        OOo 3.1

    See Also:
        `API XExternalDocLink <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sheet_1_1XExternalDocLink.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sheet.XExternalDocLink']

    def addSheetCache(self, aSheetName: str, DynamicCache: bool) -> 'XExternalSheetCache_1a420e89':
        """
        This method adds a new sheet cache instance to the external document link for a specified sheet name. If a sheet cache instance already exists for the specified name, then the existing instance is returned.
        
        Note that a sheet name lookup is performed in a case-insensitive fashion.
        """
    @property
    def TokenIndex(self) -> int:
        """
        Index corresponding to the external document link.
        
        This index value corresponds with the external document represented by an instance of com.sun.star.sheet.ExternalDocLink. This value is stored within a formula token instance.
        
        Each external document cache instance has a unique index value, and this index value can be used to retrieve the corresponding external document cache from the parent com.sun.star.sheet.ExternalDocLinks instance.
        """


