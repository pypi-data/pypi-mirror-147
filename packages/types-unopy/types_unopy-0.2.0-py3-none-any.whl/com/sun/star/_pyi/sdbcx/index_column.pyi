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
# Namespace: com.sun.star.sdbcx
from .column import Column as Column_7b1d098a

class IndexColumn(Column_7b1d098a):
    """
    Service Class

    adds a property to determine the sort order of the column values within the index.
    
    Some database drivers may ignore this property.

    See Also:
        `API IndexColumn <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sdbcx_1_1IndexColumn.html>`_
    """
    @property
    def IsAscending(self) -> bool:
        """
        is the column sorted in ascending order.
        """


