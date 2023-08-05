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
# Namespace: com.sun.star.auth
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .xsso_acceptor_context import XSSOAcceptorContext as XSSOAcceptorContext_6960e1d
    from .xsso_initiator_context import XSSOInitiatorContext as XSSOInitiatorContext_168c0e9f

class XSSOManager(XInterface_8f010a43):
    """
    supports the creation of security contexts for both the initiator/source side and the acceptor/target side.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XSSOManager <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1auth_1_1XSSOManager.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.auth.XSSOManager']

    def createAcceptorContext(self, TargetPrincipal: str) -> 'XSSOAcceptorContext_6960e1d':
        """
        creates an acceptor side security context.

        Raises:
            InvalidArgumentException: ``InvalidArgumentException``
            InvalidCredentialException: ``InvalidCredentialException``
            InvalidPrincipalException: ``InvalidPrincipalException``
            UnsupportedException: ``UnsupportedException``
        """
    def createInitiatorContext(self, SourcePrincipal: str, TargetPrincipal: str, TargetHost: str) -> 'XSSOInitiatorContext_168c0e9f':
        """
        creates an initiator side security context.

        Raises:
            InvalidArgumentException: ``InvalidArgumentException``
            InvalidCredentialException: ``InvalidCredentialException``
            InvalidPrincipalException: ``InvalidPrincipalException``
            UnsupportedException: ``UnsupportedException``
        """
    def getMechanism(self) -> str:
        """
        retrieves the mechanism name of all security contexts created using this manager.
        """

