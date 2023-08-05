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
# Namespace: com.sun.star.xml.crypto.sax
from typing_extensions import Literal
import typing
from ....uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .x_encryption_result_listener import XEncryptionResultListener as XEncryptionResultListener_290f14ea

class XEncryptionResultBroadcaster(XInterface_8f010a43):
    """
    Interface of Encryption Result Broadcaster.
    
    This interface is used to manipulate encryption result listener.

    See Also:
        `API XEncryptionResultBroadcaster <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1xml_1_1crypto_1_1sax_1_1XEncryptionResultBroadcaster.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.xml.crypto.sax.XEncryptionResultBroadcaster']

    def addEncryptionResultListener(self, listener: 'XEncryptionResultListener_290f14ea') -> None:
        """
        Adds a new encryption result listener.
        
        When the encryption is finished, the result information will be sent to this listener.

        Raises:
            com.sun.star.uno.Exception: ``Exception``
        """
    def removeEncryptionResultListener(self, listener: 'XEncryptionResultListener_290f14ea') -> None:
        """
        Removes an encryption result listener.
        
        After a listener is removed, no result information will be sent to it.
        """

