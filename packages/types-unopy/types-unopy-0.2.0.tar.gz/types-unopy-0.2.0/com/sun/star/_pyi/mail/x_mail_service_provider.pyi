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
# Namespace: com.sun.star.mail
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .mail_service_type import MailServiceType as MailServiceType_d3920ca1
    from .x_mail_service import XMailService as XMailService_ae610b57

class XMailServiceProvider(XInterface_8f010a43):
    """
    A factory for creating different mail services.
    
    **since**
    
        OOo 2.0

    See Also:
        `API XMailServiceProvider <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1mail_1_1XMailServiceProvider.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.mail.XMailServiceProvider']

    def create(self, aType: 'MailServiceType_d3920ca1') -> 'XMailService_ae610b57':
        """
        A factory method.

        Raises:
            com.sun.star.mail.NoMailServiceProviderException: ``NoMailServiceProviderException``
            com.sun.star.uno.Exception: ``Exception``
        """

