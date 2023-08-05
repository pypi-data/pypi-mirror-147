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
# Namespace: com.sun.star.document
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..io.x_input_stream import XInputStream as XInputStream_98d40ab4
    from ..io.x_output_stream import XOutputStream as XOutputStream_a4e00b35

class XBinaryStreamResolver(XInterface_8f010a43):
    """
    This interface encapsulates functionality to get/resolve binary data streams. It is used to transform binary data to a URL or to transform a URL to binary data. The binary data is represented through input and output streams.
    
    In the case of transforming a URL to binary data, the getInputStream method is used. This returns a com.sun.star.io.XInputStream from which the binary data, transformed from the given URL, can be read.
    
    In the case of transforming binary data to a URL, a com.sun.star.io.XOutputStream is created first to write the binary data to. After this, the resolveOutputStream method can be used to transform the binary data, represented through the com.sun.star.io.XOutputStream interface, to a URL.

    See Also:
        `API XBinaryStreamResolver <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1document_1_1XBinaryStreamResolver.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.document.XBinaryStreamResolver']

    def createOutputStream(self) -> 'XOutputStream_a4e00b35':
        """
        creates an output stream, to which binary data can be written.
        
        After writing, a URL can be retrieved by a call to XBinaryStreamResolver.resolveOutputStream().
        """
    def getInputStream(self, aURL: str) -> 'XInputStream_98d40ab4':
        """
        converts the given URL from the source URL namespace to an input stream, from which binary data can be read
        """
    def resolveOutputStream(self, aBinaryStream: 'XOutputStream_a4e00b35') -> str:
        """
        converts the output stream, data has been written to, to a URL in source URL namespace.
        """

