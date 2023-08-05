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
# Namespace: com.sun.star.ucb
from typing_extensions import Literal
from ..uno.x_interface import XInterface as XInterface_8f010a43

class XFileIdentifierConverter(XInterface_8f010a43):
    """
    specifies methods to convert between (file) URLs and file paths in system dependent notation.

    See Also:
        `API XFileIdentifierConverter <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1ucb_1_1XFileIdentifierConverter.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.ucb.XFileIdentifierConverter']

    def getFileProviderLocality(self, BaseURL: str) -> int:
        """
        Get information about the \"locality\" of a file content provider.
        
        The returned information can be used to chose the \"best\" among a number of file content providers implementing this interface.
        """
    def getFileURLFromSystemPath(self, BaseURL: str, SystemPath: str) -> str:
        """
        converts a file path in system dependent notation to a (file) URL.
        """
    def getSystemPathFromFileURL(self, URL: str) -> str:
        """
        converts a (file) URL to a file path in system dependent notation.
        """

