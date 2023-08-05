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
    from .x_result_set_meta_data import XResultSetMetaData as XResultSetMetaData_fb5f0da8

class XResultSetMetaDataSupplier(XInterface_8f010a43):
    """
    provides access to the meta data of a result set.
    
    The number, types, and properties of a ResultSet's columns are provided by the com.sun.star.sdbc.XResultSetMetaData interface returned by the com.sun.star.sdbc.XResultSetMetaDataSupplier.getMetaData() method.

    See Also:
        `API XResultSetMetaDataSupplier <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sdbc_1_1XResultSetMetaDataSupplier.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sdbc.XResultSetMetaDataSupplier']

    def getMetaData(self) -> 'XResultSetMetaData_fb5f0da8':
        """
        retrieves the number, types, and properties of a ResultSet's columns.

        Raises:
            SQLException: ``SQLException``
        """

