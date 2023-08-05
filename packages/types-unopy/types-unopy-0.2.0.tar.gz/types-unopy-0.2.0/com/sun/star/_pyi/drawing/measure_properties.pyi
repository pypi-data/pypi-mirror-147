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
    from .measure_kind import MeasureKind as MeasureKind_c99e0c4c
    from .measure_text_horz_pos import MeasureTextHorzPos as MeasureTextHorzPos_2bcb0f40
    from .measure_text_vert_pos import MeasureTextVertPos as MeasureTextVertPos_2bd90f3e

class MeasureProperties(ABC):
    """
    Service Class

    This service describes a MeasureShape.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API MeasureProperties <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1drawing_1_1MeasureProperties.html>`_
    """
    @property
    def MeasureBelowReferenceEdge(self) -> bool:
        """
        If this property is TRUE, the measure is drawn below the reference edge instead of above it.
        """
    @property
    def MeasureDecimalPlaces(self) -> int:
        """
        This value is the number of decimal places that is used to format the measure value.
        
        **since**
        
            OOo 1.1.2
        """
    @property
    def MeasureHelpLine1Length(self) -> int:
        """
        This is the length of the first help line.
        """
    @property
    def MeasureHelpLine2Length(self) -> int:
        """
        This is the length of the second help line.
        """
    @property
    def MeasureHelpLineDistance(self) -> int:
        """
        This is the distance from the measure line to the start of the help lines.
        """
    @property
    def MeasureHelpLineOverhang(self) -> int:
        """
        This is the overhang of the two help lines.
        """
    @property
    def MeasureKind(self) -> 'MeasureKind_c99e0c4c':
        """
        This enumeration specifies the MeasureKind.
        """
    @property
    def MeasureLineDistance(self) -> int:
        """
        This is the distance from the reference edge to the measure line.
        """
    @property
    def MeasureOverhang(self) -> int:
        """
        This is the overhang of the reference line over the help lines.
        """
    @property
    def MeasureShowUnit(self) -> bool:
        """
        If this is TRUE, the unit of measure is shown in the measure text.
        """
    @property
    def MeasureTextAutoAngle(self) -> bool:
        """
        If this is TRUE, the angle of the measure is set automatically.
        """
    @property
    def MeasureTextAutoAngleView(self) -> int:
        """
        This is the automatic angle.
        """
    @property
    def MeasureTextFixedAngle(self) -> int:
        """
        This is the fixed angle.
        """
    @property
    def MeasureTextHorizontalPosition(self) -> 'MeasureTextHorzPos_2bcb0f40':
        """
        This is the horizontal position of the measure text.
        """
    @property
    def MeasureTextIsFixedAngle(self) -> bool:
        """
        If this value is TRUE, the measure has a fixed angle.
        """
    @property
    def MeasureTextRotate90(self) -> bool:
        """
        If this value is TRUE, the text is rotated 90 degrees.
        """
    @property
    def MeasureTextUpsideDown(self) -> bool:
        """
        If this value is TRUE, the text is printed upside down.
        """
    @property
    def MeasureTextVerticalPosition(self) -> 'MeasureTextVertPos_2bd90f3e':
        """
        This is the vertical position of the text.
        """


