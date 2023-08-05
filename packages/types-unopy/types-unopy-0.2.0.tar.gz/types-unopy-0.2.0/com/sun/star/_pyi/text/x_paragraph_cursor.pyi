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
# Namespace: com.sun.star.text
from typing_extensions import Literal
from .x_text_cursor import XTextCursor as XTextCursor_a60c0b48

class XParagraphCursor(XTextCursor_a60c0b48):
    """
    makes it possible to move paragraph by paragraph.

    See Also:
        `API XParagraphCursor <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XParagraphCursor.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.text.XParagraphCursor']

    def gotoEndOfParagraph(self, bExpand: bool) -> bool:
        """
        moves the cursor to the end of the current paragraph.
        """
    def gotoNextParagraph(self, bExpand: bool) -> bool:
        """
        moves the cursor to the next paragraph.
        """
    def gotoPreviousParagraph(self, bExpand: bool) -> bool:
        """
        moves the cursor to the previous paragraph.
        """
    def gotoStartOfParagraph(self, bExpand: bool) -> bool:
        """
        moves the cursor to the start of the current paragraph.
        """
    def isEndOfParagraph(self) -> bool:
        """
        determines if the cursor is positioned at the end of a paragraph.
        """
    def isStartOfParagraph(self) -> bool:
        """
        determines if the cursor is positioned at the start of a paragraph.
        """

