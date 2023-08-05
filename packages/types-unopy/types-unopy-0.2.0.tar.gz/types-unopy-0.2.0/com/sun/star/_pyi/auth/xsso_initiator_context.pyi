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
from .xsso_context import XSSOContext as XSSOContext_a2840aec

class XSSOInitiatorContext(XSSOContext_a2840aec):
    """
    represents an initiator side security context.
    
    This context may be used to initialize authentication tokens to send to an acceptor and to authenticate any token sent back in response.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XSSOInitiatorContext <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1auth_1_1XSSOInitiatorContext.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.auth.XSSOInitiatorContext']

    def init(self, Token: 'typing.Tuple[int, ...]') -> 'typing.Tuple[int, ...]':
        """
        initializes an SSO Token to send to the acceptor side and authenticates an SSO Token returned by the acceptor if the context supports mutual authentication.
        
        init should be called only once for contexts which don't support mutual authentication and at most twice for contexts which do support mutual authentication. Additional calls produce undefined results.

        Raises:
            InvalidArgumentException: ``InvalidArgumentException``
            InvalidCredentialException: ``InvalidCredentialException``
            InvalidContextException: ``InvalidContextException``
            AuthenticationFailedException: ``AuthenticationFailedException``
        """

