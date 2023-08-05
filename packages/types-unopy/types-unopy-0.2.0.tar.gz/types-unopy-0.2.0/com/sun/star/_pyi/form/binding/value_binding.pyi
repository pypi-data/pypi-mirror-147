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
from ...beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from .x_value_binding import XValueBinding as XValueBinding_271b0ed5
from ...lang.x_component import XComponent as XComponent_98dc0ab5
from ...util.x_modify_broadcaster import XModifyBroadcaster as XModifyBroadcaster_fd990df0

class ValueBinding(XPropertySet_bc180bfa, XValueBinding_271b0ed5, XComponent_98dc0ab5, XModifyBroadcaster_fd990df0):
    """
    Service Class

    defines a component which allows access to a single value
    
    Read/Write access to the value represented by this component is supported, as well as (optionally) active broadcasting of value changes

    See Also:
        `API ValueBinding <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1form_1_1binding_1_1ValueBinding.html>`_
    """
    @property
    def ReadOnly(self) -> bool:
        """
        determines whether the value is currently readonly
        
        For instance, you could imagine a ValueBinding which represents a cell in a spreadsheet document, and whose value is readonly as long as the spreadsheet is locked.
        
        As long as this property is TRUE, the value binding should throw an InvalidBindingStateException when its XValueBinding.setValue() method is invoked.
        """
    @property
    def Relevant(self) -> bool:
        """
        determines the relevance of the value represented by the binding
        
        In a more complex scenario, where different form controls are bound to different values, which all are part of a larger data structure, some of the items in this data structure may not be relevant currently. This is indicated by the Relevant property being FALSE.
        
        XBindableValues which are bound to this binding may or may not react in certain ways on the (ir)relevance of their bound value.
        
        One possible reaction could be that user interface elements which are associated with the XBindableValue are disabled as long as Relevant is FALSE.
        """


