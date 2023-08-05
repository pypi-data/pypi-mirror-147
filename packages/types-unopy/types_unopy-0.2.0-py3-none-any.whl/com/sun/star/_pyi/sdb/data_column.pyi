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
# Service Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.sdb
from .result_column import ResultColumn as ResultColumn_a4980b2e
from .x_column import XColumn as XColumn_70650907
from .x_column_update import XColumnUpdate as XColumnUpdate_aebd0b6a

class DataColumn(ResultColumn_a4980b2e, XColumn_70650907, XColumnUpdate_aebd0b6a):
    """
    Service Class

    defines a column used for a result set which contains the data definition and the data of the column of the current row of a result set.

    See Also:
        `API DataColumn <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sdb_1_1DataColumn.html>`_
    """
    @property
    def OriginalValue(self) -> object:
        """
        contains the original value of the column.
        """
    @property
    def Value(self) -> object:
        """
        contains the column's value.
        
        This could be a constraint property, to veto modifications, if a new value does not fit into rules defined for the column.
        """


