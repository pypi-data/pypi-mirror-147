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
# Namespace: com.sun.star.table
import typing
from ..form.binding.value_binding import ValueBinding as ValueBinding_18de0e7d
from ..lang.x_initialization import XInitialization as XInitialization_d46c0cca
if typing.TYPE_CHECKING:
    from .cell_address import CellAddress as CellAddress_ae5f0b56

class CellValueBinding(ValueBinding_18de0e7d, XInitialization_d46c0cca):
    """
    Service Class

    defines the binding to a single cell in a table document
    
    Read/Write access to the cell represented by this component is supported, as well as active broadcasting of value changes.
    
    The binding supports exchanging double values, string values.
    
    The component cannot be instantiated at a global service factory, instead it's usually provided by a document instance.

    See Also:
        `API CellValueBinding <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1table_1_1CellValueBinding.html>`_
    """
    @property
    def BoundCell(self) -> 'CellAddress_ae5f0b56':
        """
        specifies the cell within a document whose value is reflected by the binding.
        """


