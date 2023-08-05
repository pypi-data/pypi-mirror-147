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
# Namespace: com.sun.star.sheet
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..text.x_text import XText as XText_690408ca

class XHeaderFooterContent(XInterface_8f010a43):
    """
    provides access to the text contents of a header or footer on a page.

    See Also:
        `API XHeaderFooterContent <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sheet_1_1XHeaderFooterContent.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sheet.XHeaderFooterContent']

    def getCenterText(self) -> 'XText_690408ca':
        """
        returns the text which is printed in the center part of the header or footer.
        """
    def getLeftText(self) -> 'XText_690408ca':
        """
        returns the text which is printed in the left part of the header or footer.
        """
    def getRightText(self) -> 'XText_690408ca':
        """
        returns the text which is printed in the right part of the header or footer.
        """

