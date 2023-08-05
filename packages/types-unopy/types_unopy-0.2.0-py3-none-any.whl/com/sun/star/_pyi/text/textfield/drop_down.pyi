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
import typing
from ..text_field import TextField as TextField_90260a56

class DropDown(TextField_90260a56):
    """
    Service Class

    specifies service of an author text field.

    See Also:
        `API DropDown <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1text_1_1textfield_1_1DropDown.html>`_
    """
    @property
    def Items(self) -> 'typing.Tuple[str, ...]':
        """
        The items of the dropdown field.
        """
    @property
    def Name(self) -> str:
        """
        The name of the drop down field.
        """
    @property
    def SelectedItem(self) -> str:
        """
        The selected item.
        
        If no item is selected this property contains an empty string. If this property is set to a value not present in the items of the dropdown field it is invalidated, i.e. it is set to an empty string.
        """


