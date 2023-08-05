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
# Namespace: com.sun.star.sdbcx
from typing_extensions import Literal
from ..uno.x_interface import XInterface as XInterface_8f010a43

class XAuthorizable(XInterface_8f010a43):
    """
    is used for accessing and setting the permissions of a user for a database object.

    See Also:
        `API XAuthorizable <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sdbcx_1_1XAuthorizable.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sdbcx.XAuthorizable']

    def getGrantablePrivileges(self, objName: str, objType: int) -> int:
        """
        retrieves the permissions for a specific object, which could be granted to other users and groups.

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """
    def getPrivileges(self, objName: str, objType: int) -> int:
        """
        retrieves the permissions for a specific object.

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """
    def grantPrivileges(self, objName: str, objType: int, objPrivileges: int) -> None:
        """
        adds additional permissions for a specific object.

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """
    def revokePrivileges(self, objName: str, objType: int, objPrivileges: int) -> None:
        """
        removes permissions for a specific object from a group or user.

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """

