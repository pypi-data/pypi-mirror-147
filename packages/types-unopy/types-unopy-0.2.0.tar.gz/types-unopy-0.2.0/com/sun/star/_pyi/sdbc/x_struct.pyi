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
# Namespace: com.sun.star.sdbc
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..container.x_name_access import XNameAccess as XNameAccess_e2ab0cf6

class XStruct(XInterface_8f010a43):
    """
    is used for the standard mapping for a SQL structured type.
    
    A Struct object contains a value for each attribute of the SQL structured type that it represents. By default, an instance of Struct is valid as long as the application has a reference to it.

    See Also:
        `API XStruct <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sdbc_1_1XStruct.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sdbc.XStruct']

    def getAttributes(self, typeMap: 'XNameAccess_e2ab0cf6') -> 'typing.Tuple[object, ...]':
        """
        produces the ordered values of the attributes of the SQL structured type that this Struct object represents.
        
        This method uses the given type map for customizations of the type mappings. If there is no entry in the given type map that matches or the given type map is NULL , the structured type that this Struct object represents, the driver uses the connection type mapping.

        Raises:
            SQLException: ``SQLException``
        """
    def getSQLTypeName(self) -> str:
        """
        retrieves the SQL type name of the SQL structured type that this Struct object represents.

        Raises:
            SQLException: ``SQLException``
        """

