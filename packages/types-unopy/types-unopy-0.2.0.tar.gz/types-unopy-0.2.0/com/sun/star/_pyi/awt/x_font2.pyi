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
# Namespace: com.sun.star.awt
from typing_extensions import Literal
from .x_font import XFont as XFont_5f480843

class XFont2(XFont_5f480843):
    """
    extends the XFont interface and provides additional information for a font.
    
    **since**
    
        OOo 3.0

    See Also:
        `API XFont2 <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XFont2.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.awt.XFont2']

    def hasGlyphs(self, aText: str) -> bool:
        """
        checks whether or not this font has all the glyphs for the text specified by aText.
        """

