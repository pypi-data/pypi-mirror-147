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
# Namespace: com.sun.star.text.textfield
from ..text_field import TextField as TextField_90260a56

class TableFormula(TextField_90260a56):
    """
    Service Class

    specifies service of a table formula text field.
    
    .. deprecated::
    
        Class is deprecated.

    See Also:
        `API TableFormula <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1text_1_1textfield_1_1TableFormula.html>`_
    """
    @property
    def CurrentPresentation(self) -> str:
        """
        contains the current content of the text field.
        
        This property is especially useful for import/export purposes.
        """
    @property
    def Formula(self) -> str:
        """
        contains the formula.
        """
    @property
    def IsShowFormula(self) -> bool:
        """
        determines whether the formula displayed as text or evaluated.
        """
    @property
    def NumberFormat(self) -> int:
        """
        this is the number format for this field.
        """


