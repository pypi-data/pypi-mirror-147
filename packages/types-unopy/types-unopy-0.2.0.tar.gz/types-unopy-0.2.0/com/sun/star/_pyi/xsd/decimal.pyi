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
# Namespace: com.sun.star.xsd
from .x_data_type import XDataType as XDataType_83f209cb

class Decimal(XDataType_83f209cb):
    """
    Service Class

    specifies an XSD compliant decimal type

    See Also:
        `API Decimal <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1xsd_1_1Decimal.html>`_
    """
    @property
    def FractionDigits(self) -> int:
        """
        fractionDigits is the maximum number of digits in the fractional part of values of decimal data
        
        The value of fractionDigits must be a non negative integer.
        
        See http://www.w3.org/TR/xmlschema-2/#rf-fractionDigits
        """
    @property
    def MaxExclusiveDouble(self) -> float:
        """
        specifies the exclusive upper bound for the value
        """
    @property
    def MaxInclusiveDouble(self) -> float:
        """
        specifies the inclusive upper bound for the value
        """
    @property
    def MinExclusiveDouble(self) -> float:
        """
        specifies the exclusive lower bound for the value
        """
    @property
    def MinInclusiveDouble(self) -> float:
        """
        specifies the inclusive lower bound for the value
        """
    @property
    def TotalDigits(self) -> int:
        """
        totalDigits is the maximum number of digits in values of decimal data types.
        
        The value of totalDigits must be a positive integer.
        
        See http://www.w3.org/TR/xmlschema-2/#rf-totalDigits
        """


