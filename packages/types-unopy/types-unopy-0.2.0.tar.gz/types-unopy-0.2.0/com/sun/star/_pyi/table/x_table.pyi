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
# Namespace: com.sun.star.table
from typing_extensions import Literal
import typing
from ..beans.x_fast_property_set import XFastPropertySet as XFastPropertySet_ee6b0d88
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from ..lang.x_component import XComponent as XComponent_98dc0ab5
from .x_cell_range import XCellRange as XCellRange_a2f70ad5
from .x_column_row_range import XColumnRowRange as XColumnRowRange_e0e70cfb
from ..util.x_modifiable import XModifiable as XModifiable_a4f60b0a
if typing.TYPE_CHECKING:
    from .x_cell_cursor import XCellCursor as XCellCursor_ae900b66

class XTable(XFastPropertySet_ee6b0d88, XPropertySet_bc180bfa, XComponent_98dc0ab5, XCellRange_a2f70ad5, XColumnRowRange_e0e70cfb, XModifiable_a4f60b0a):
    """

    See Also:
        `API XTable <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1table_1_1XTable.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.table.XTable']

    def createCursor(self) -> 'XCellCursor_ae900b66':
        """
        creates a cell cursor including the whole table
        """
    def createCursorByRange(self, Range: 'XCellRange_a2f70ad5') -> 'XCellCursor_ae900b66':
        """
        creates a cell cursor to travel in the given range context.

        Raises:
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    @property
    def ColumnCount(self) -> int:
        """
        stores the current column count of this table
        """

    @property
    def RowCount(self) -> int:
        """
        stores the current row count of this table
        """


