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
# Namespace: com.sun.star.form.inspection
from ...inspection.x_object_inspector_model import XObjectInspectorModel as XObjectInspectorModel_9077119b

class DefaultFormComponentInspectorModel(XObjectInspectorModel_9077119b):
    """
    Service Class

    implements a com.sun.star.inspection.XObjectInspectorModel for inspecting form components, in particular all components implementing the FormComponent service.
    
    A DefaultFormComponentInspectorModel provides the following handlers by default:
    
    **since**
    
        OOo 2.2

    See Also:
        `API DefaultFormComponentInspectorModel <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1form_1_1inspection_1_1DefaultFormComponentInspectorModel.html>`_
    """
    def createDefault(self) -> None:
        """
        creates a default DefaultFormComponentInspectorModel, providing factories for all handlers listed above.
        
        **since**
        
            OOo 2.2
        """
    def createWithHelpSection(self, minHelpTextLines: int, maxHelpTextLines: int) -> None:
        """
        creates a default DefaultFormComponentInspectorModel, providing factories for all handlers listed above, and describing an ObjectInspector which has a help section.
        
        **since**
        
            OOo 2.2

        Raises:
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """


