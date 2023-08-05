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
# Namespace: com.sun.star.inspection
from typing_extensions import Literal
import typing
from ..frame.x_controller import XController as XController_b00e0b8f
from ..frame.x_dispatch_provider import XDispatchProvider as XDispatchProvider_fc690de6
if typing.TYPE_CHECKING:
    from .x_object_inspector_model import XObjectInspectorModel as XObjectInspectorModel_9077119b
    from .x_object_inspector_ui import XObjectInspectorUI as XObjectInspectorUI_5ccd1048
    from ..uno.x_interface import XInterface as XInterface_8f010a43

class XObjectInspector(XController_b00e0b8f, XDispatchProvider_fc690de6):
    """
    describes the main interface of an ObjectInspector.
    
    **since**
    
        OOo 2.0.3

    See Also:
        `API XObjectInspector <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1inspection_1_1XObjectInspector.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.inspection.XObjectInspector']

    def inspect(self, Objects: 'typing.Tuple[XInterface_8f010a43, ...]') -> None:
        """
        inspects a new collection of one or more objects.
        
        If the sequence is empty, the UI of the ObjectInspector will be cleared.
        
        If the sequence contains more than one object, the XObjectInspector will create a complete set of property handlers (as indicated by XObjectInspectorModel.HandlerFactories) for every of the objects, and compose their output.

        Raises:
            com.sun.star.util.VetoException: ``VetoException``
        """
    @property
    def InspectorModel(self) -> 'XObjectInspectorModel_9077119b':
        """
        provides access to the current model of the inspector
        
        The model is mainly responsible for providing the property handlers. Additionally, it can provide user interface names and help URLs for property categories.
        
        Note that there are two ways of setting or retrieving the current model: You can either use com.sun.star.frame.XModel.setModel(), or, if you do not want or need to implement the full-blown com.sun.star.frame.XModel interface, you can use this property directly. Both approaches are semantically equivalent.
        
        If a new model is set at the inspector, the complete UI will be rebuilt to reflect the change, using the new property handlers provided by the new model.
        """

    @property
    def InspectorUI(self) -> 'XObjectInspectorUI_5ccd1048':
        """
        provides access to the user interface of the object inspector.
        
        This interface can be used to access and manipulate various aspects of the user interface. For instance, you can enable and disable certain property controls (or parts thereof), or register observers for all property controls.
        
        **since**
        
            OOo 2.2
        """


