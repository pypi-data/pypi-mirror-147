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
# Namespace: com.sun.star.form.binding
from .bindable_data_aware_control_model import BindableDataAwareControlModel as BindableDataAwareControlModel_47091512
from ..component.database_combo_box import DatabaseComboBox as DatabaseComboBox_7ac510eb

class BindableDatabaseComboBox(BindableDataAwareControlModel_47091512, DatabaseComboBox_7ac510eb):
    """
    Service Class

    This service specifies a model of a combo box (a list box combined with a text input field) which is data-aware and thus can be bound to a database field, and additionally supports binding to arbitrary external values.
    
    If a com.sun.star.form.binding.ValueBinding instance is set at the field, it will exchange it's text with the binding as string, thus only bindings supporting string exchange will be accepted in com.sun.star.form.binding.XValueBinding.setValueBinding().

    See Also:
        `API BindableDatabaseComboBox <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1form_1_1binding_1_1BindableDatabaseComboBox.html>`_
    """


