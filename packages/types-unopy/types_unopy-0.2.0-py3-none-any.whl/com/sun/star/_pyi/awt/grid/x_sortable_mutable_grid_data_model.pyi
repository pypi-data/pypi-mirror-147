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
# Namespace: com.sun.star.awt.grid
from typing_extensions import Literal
from .x_mutable_grid_data_model import XMutableGridDataModel as XMutableGridDataModel_6387103b
from .x_sortable_grid_data import XSortableGridData as XSortableGridData_25fa0ebc

class XSortableMutableGridDataModel(XMutableGridDataModel_6387103b, XSortableGridData_25fa0ebc):
    """
    describes a grid control data model whose data can be modified and sorted.

    See Also:
        `API XSortableMutableGridDataModel <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1grid_1_1XSortableMutableGridDataModel.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.awt.grid.XSortableMutableGridDataModel']


