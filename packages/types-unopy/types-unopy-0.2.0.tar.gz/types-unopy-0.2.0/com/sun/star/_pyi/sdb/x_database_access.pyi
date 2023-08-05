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
# Namespace: com.sun.star.sdb
from typing_extensions import Literal
import typing
from ..sdbc.x_data_source import XDataSource as XDataSource_a2990ae7
if typing.TYPE_CHECKING:
    from .x_database_access_listener import XDatabaseAccessListener as XDatabaseAccessListener_32d80f46
    from ..sdbc.x_connection import XConnection as XConnection_a36a0b0c

class XDatabaseAccess(XDataSource_a2990ae7):
    """
    is not to be used anymore
    
    .. deprecated::
    
        Class is deprecated.

    See Also:
        `API XDatabaseAccess <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sdb_1_1XDatabaseAccess.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sdb.XDatabaseAccess']

    def addDatabaseAccessListener(self, listener: 'XDatabaseAccessListener_32d80f46') -> None:
        """
        """
    def getIsolatedConnection(self, user: str, password: str) -> 'XConnection_a36a0b0c':
        """

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """
    def hasConnections(self) -> bool:
        """
        """
    def removeDatabaseAccessListener(self, listener: 'XDatabaseAccessListener_32d80f46') -> None:
        """
        """
    def suspendConnections(self) -> bool:
        """

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """

