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
# Namespace: com.sun.star.embed
from typing_extensions import Literal
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from .x_encryption_protected_source import XEncryptionProtectedSource as XEncryptionProtectedSource_8cdf11a3
from .x_transacted_object import XTransactedObject as XTransactedObject_fb510dbd
from .x_transaction_broadcaster import XTransactionBroadcaster as XTransactionBroadcaster_576e104d
from ..io.x_seekable import XSeekable as XSeekable_79540954
from ..io.x_stream import XStream as XStream_678908a4
from ..lang.x_component import XComponent as XComponent_98dc0ab5

class XExtendedStorageStream(XPropertySet_bc180bfa, XEncryptionProtectedSource_8cdf11a3, XTransactedObject_fb510dbd, XTransactionBroadcaster_576e104d, XSeekable_79540954, XStream_678908a4, XComponent_98dc0ab5):
    """
    This interface allows access to an extended storage stream that might be transacted.

    See Also:
        `API XExtendedStorageStream <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1embed_1_1XExtendedStorageStream.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.embed.XExtendedStorageStream']


