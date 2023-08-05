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
from ..uno.x_interface import XInterface as XInterface_8f010a43

class XTypeDetection(XInterface_8f010a43):
    """
    support \"flat\" and \"deep\" type detection of a given document
    
    A \"flat\" detection means specifying the document format by using the URL and some configuration data only. That will perform but produce may invalid results if e.g., the extension of the document is wrong. A \"deep\" detection means looking into the document stream to be right which format it supports. Of course that includes a \"flat\" detection before. The combination of both ones should produce stable results every time.

    See Also:
        `API XTypeDetection <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1document_1_1XTypeDetection.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.document.XTypeDetection']

    def queryTypeByDescriptor(self, Descriptor: object, AllowDeep: bool) -> str:
        """
        make a \"deep\" detection or optional a \"flat\" detection by using a MediaDescriptor
        
        Instead of XTypeDetection.queryTypeByURL() this function use a MediaDescriptor to specify the document for detection. Such descriptor hold different information about the document. He will be passed to any part of made detection process and every part can change it to actualize it. The property MediaDescriptor.URL should be set on this descriptor as minimum. It specifies the location of the document. If this parameter is missing another one is required: MediaDescriptor.InputStream. This can be useful to prevent operation against multiple opening of the stream and perform the operation. If this stream isn't already included the detection will open it (if allowed!) and add it to the descriptor so it will be available for all following parts. A combination of both parameters can be useful to perform the operation and make results more stable; but only one of them is required. Of course its possible to specify more document properties (e.g. MediaDescriptor.ReadOnly).
        As an additional feature it's possible to suppress \"deep\" detection by using argument AllowDeep.
        """
    def queryTypeByURL(self, URL: str) -> str:
        """
        make a \"flat\" detection by using the URL of the document
        
        It use given URL in combination with the internal configuration of well known types only to specify the format of given document.
        """

