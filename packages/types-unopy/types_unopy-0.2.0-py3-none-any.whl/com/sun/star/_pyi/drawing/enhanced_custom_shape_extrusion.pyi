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
# Namespace: com.sun.star.drawing
import typing
from abc import ABC
if typing.TYPE_CHECKING:
    from .direction3_d import Direction3D as Direction3D_c9370c0c
    from .enhanced_custom_shape_parameter_pair import EnhancedCustomShapeParameterPair as EnhancedCustomShapeParameterPair_262914a3
    from .position3_d import Position3D as Position3D_bddc0bc0
    from .projection_mode import ProjectionMode as ProjectionMode_f1ff0d96
    from .shade_mode import ShadeMode as ShadeMode_b0c60b5e

class EnhancedCustomShapeExtrusion(ABC):
    """
    Service Class

    This service may be represented by a com.sun.star.beans.PropertyValue [].

    See Also:
        `API EnhancedCustomShapeExtrusion <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1drawing_1_1EnhancedCustomShapeExtrusion.html>`_
    """
    @property
    def Brightness(self) -> float:
        """
        This attribute specifies the brightness of a scene in percent.
        """
    @property
    def Depth(self) -> 'EnhancedCustomShapeParameterPair_262914a3':
        """
        The first value of EnhancedCustomShapeParameterPair specifies the depth of the extrusion in 1/100 mm.
        
        The second value (0.0 to 1.0) specifies the fraction of the extrusion that lies before the shape, a value of 0 is default.
        """
    @property
    def Diffusion(self) -> float:
        """
        This attribute specifies the amount of diffusion reflected by the shape in percent.
        """
    @property
    def Extrusion(self) -> bool:
        """
        This property specifies if extrusion is displayed.
        
        The default for this property is \"false\"
        """
    @property
    def ExtrusionColor(self) -> bool:
        """
        This attribute specifies if the \"SecondFillColor\" is used as extrusion color.
        """
    @property
    def FirstLightDirection(self) -> 'Direction3D_c9370c0c':
        """
        Specifies the direction of the first light.
        """
    @property
    def FirstLightHarsh(self) -> bool:
        """
        Specifies if the primary light is harsh.
        """
    @property
    def FirstLightLevel(self) -> float:
        """
        Specifies the intensity for the first light in percent.
        """
    @property
    def LightFace(self) -> bool:
        """
        Specifies if the front face of the extrusion responds to lightning changes.
        """
    @property
    def Metal(self) -> bool:
        """
        Specifies if the surface of the extrusion object looks like metal.
        """
    @property
    def NumberOfLineSegments(self) -> int:
        """
        Specifies the number of line segments that should be used to display curved surfaces.
        
        The higher the number the more line segments are used.
        """
    @property
    def Origin(self) -> 'EnhancedCustomShapeParameterPair_262914a3':
        """
        This attribute specifies the origin within the bounding box of the shape in terms of the shape size fractions.
        """
    @property
    def ProjectionMode(self) -> 'ProjectionMode_f1ff0d96':
        """
        This property defines the projection mode.
        """
    @property
    def RotateAngle(self) -> 'EnhancedCustomShapeParameterPair_262914a3':
        """
        This attributes specifies the rotation angle about the x-axis in grad.
        
        The order of rotation is: z-axis, y-axis and then x-axis. The z-axis is specified by the draw:rotate-angle.
        """
    @property
    def RotationCenter(self) -> 'Direction3D_c9370c0c':
        """
        This attribute specifies the position of the rotate center in terms of shape size fractions, if the property is omitted, then the geometrical center of the shape is used (this is the default).
        """
    @property
    def SecondLightDirection(self) -> 'Direction3D_c9370c0c':
        """
        Specifies the direction of the second light.
        """
    @property
    def SecondLightHarsh(self) -> bool:
        """
        Specifies if the secondary light is harsh.
        """
    @property
    def SecondLightLevel(self) -> float:
        """
        Specifies the intensity for the second light in percent.
        """
    @property
    def ShadeMode(self) -> 'ShadeMode_b0c60b5e':
        """
        This property defines the shade mode.
        """
    @property
    def Shininess(self) -> float:
        """
        The draw:extrusion-shininess specifies the shininess of a mirror in percent.
        """
    @property
    def Skew(self) -> 'EnhancedCustomShapeParameterPair_262914a3':
        """
        The first value of the draw:extrusion-skew attribute specifies the skew amount of an extrusion in percent.
        
        The second parameter specifies the skew-angle. Skew settings are only applied if the attribute ProjectionMode is ProjectionMode_PARALLEL.
        """
    @property
    def Specularity(self) -> float:
        """
        This attribute specifies the specularity of an extrusion object in percent.
        """
    @property
    def ViewPoint(self) -> 'Position3D_bddc0bc0':
        """
        This attribute specifies the viewpoint of the observer.
        """


