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
# Namespace: com.sun.star.graphic
import typing
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from .x_graphic_renderer import XGraphicRenderer as XGraphicRenderer_aca0e33
if typing.TYPE_CHECKING:
    from ..awt.rectangle import Rectangle as Rectangle_84b109e9

class GraphicRendererVCL(XPropertySet_bc180bfa, XGraphicRenderer_aca0e33):
    """
    Service Class

    Service that describes the necessary interfaces and properties to render a graphic container of XGraphic type.
    
    To render a XGraphic container, just create an instance of this service, set the appropriate properties and use the XGraphicRenderer interface to initiate the rendering process itself

    See Also:
        `API GraphicRendererVCL <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1graphic_1_1GraphicRendererVCL.html>`_
    """
    @property
    def DestinationRect(self) -> 'Rectangle_84b109e9':
        """
        Specifies the destination rectangle, into which the graphic content is to be rendered onto the device.
        """
    @property
    def Device(self) -> object:
        """
        Holds the device onto which the XGraphic container should be rendered.
        
        In case of using VCL Devices, this property should hold a com.sun.star.awt.XDevice interface
        """
    @property
    def RenderData(self) -> object:
        """
        Additional properties for rendering, unspecified at the moment.
        """


