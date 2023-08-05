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
# Namespace: com.sun.star.sheet
from abc import ABC

class RangeSelectionArguments(ABC):
    """
    Service Class

    contains the arguments for starting the range selection.
    
    **since**
    
        OOo 2.0.3

    See Also:
        `API RangeSelectionArguments <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sheet_1_1RangeSelectionArguments.html>`_
    """
    @property
    def CloseOnMouseRelease(self) -> bool:
        """
        specifies if the range selection is finished when the mouse button is released, after selecting cells.
        """
    @property
    def InitialValue(self) -> str:
        """
        contains the initial value for the range descriptor.
        """
    @property
    def SingleCellMode(self) -> bool:
        """
        specifies if the range selection is limited to a single cell only.
        
        If TRUE, the selection is restricted to a single cell. If FALSE, multiple adjoining cells can be selected. The default value is FALSE.
        
        **since**
        
            OOo 2.0.3
        """
    @property
    def Title(self) -> str:
        """
        contains a title for the operation.
        """


