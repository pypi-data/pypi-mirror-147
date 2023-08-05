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
# Namespace: com.sun.star.script
from typing_extensions import Literal
import typing
from .x_invocation import XInvocation as XInvocation_be070c0f
if typing.TYPE_CHECKING:
    from .invocation_info import InvocationInfo as InvocationInfo_e5270d43

class XInvocation2(XInvocation_be070c0f):
    """
    Extension of XInvocation to provide additional information about the methods and properties that are accessible via XInvocation.

    See Also:
        `API XInvocation2 <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1script_1_1XInvocation2.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.script.XInvocation2']

    def getInfo(self) -> 'typing.Tuple[InvocationInfo_e5270d43, ...]':
        """
        returns information items for all methods and properties accessible via XInvocation.
        """
    def getInfoForName(self, aName: str, bExact: bool) -> 'InvocationInfo_e5270d43':
        """
        returns information item for the method or property defined by aName

        Raises:
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    def getMemberNames(self) -> 'typing.Tuple[str, ...]':
        """
        returns the names of all methods and properties accessible via XInvocation.
        """

