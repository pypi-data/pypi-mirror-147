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
# Struct Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.sheet
# Libre Office Version: 7.3
from typing_extensions import Literal
import typing


class TablePageBreakData(object):
    """
    Struct Class

    describes a page break in a spreadsheet.

    See Also:
        `API TablePageBreakData <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1sheet_1_1TablePageBreakData.html>`_
    """
    typeName: Literal['com.sun.star.sheet.TablePageBreakData']

    def __init__(self, Position: typing.Optional[int] = ..., ManualBreak: typing.Optional[bool] = ...) -> None:
        """
        Constructor

        Arguments:
            Position (int, optional): Position value.
            ManualBreak (bool, optional): ManualBreak value.
        """


    @property
    def Position(self) -> int:
        """
        the position (column or row index) of the page break.
        """


    @property
    def ManualBreak(self) -> bool:
        """
        is TRUE for a manual page break, FALSE for an automatic one.
        """


