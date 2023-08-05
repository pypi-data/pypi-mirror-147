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
# Namespace: com.sun.star.chart2
from typing_extensions import Literal
import typing
from .x_formatted_string2 import XFormattedString2 as XFormattedString2_8010df3
if typing.TYPE_CHECKING:
    from .data_point_custom_label_field_type import DataPointCustomLabelFieldType as DataPointCustomLabelFieldType_cc7712b1

class XDataPointCustomLabelField(XFormattedString2_8010df3):
    """
    Provides interface for DataPointCustomLabelField service.
    
    **since**
    
        LibreOffice 6.1

    See Also:
        `API XDataPointCustomLabelField <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1chart2_1_1XDataPointCustomLabelField.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.chart2.XDataPointCustomLabelField']

    def getCellRange(self) -> str:
        """
        Returns the address of the cell[range] from which the content of this field is sourced.
        
        **since**
        
            LibreOffice 7.3
        """
    def getDataLabelsRange(self) -> bool:
        """
        Indicates whether the label field's content is sourced from a cell[range] or not.
        
        **since**
        
            LibreOffice 7.3
        """
    def getFieldType(self) -> 'DataPointCustomLabelFieldType_cc7712b1':
        """
        """
    def getGuid(self) -> str:
        """
        """
    def setCellRange(self, cellRange: str) -> None:
        """
        Sets the address of the cell[range] from which the content of this field is sourced.
        
        **since**
        
            LibreOffice 7.3
        """
    def setDataLabelsRange(self, dataLabelsRange: bool) -> None:
        """
        Sets whether the label field's content is sourced from a cell[range] or not.
        
        **since**
        
            LibreOffice 7.3
        """
    def setFieldType(self, fieldType: 'DataPointCustomLabelFieldType_cc7712b1') -> None:
        """
        """
    def setGuid(self, guid: str) -> None:
        """
        """

