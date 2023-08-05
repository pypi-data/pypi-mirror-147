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
# Namespace: com.sun.star.graphic
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..beans.property_value import PropertyValue as PropertyValue_c9610c73
    from ..geometry.real_rectangle2_d import RealRectangle2D as RealRectangle2D_d9b0e03
    from .x_primitive2_d import XPrimitive2D as XPrimitive2D_d5730c6d
    from ..rendering.x_bitmap import XBitmap as XBitmap_b1b70b7b

class XPrimitive2DRenderer(XInterface_8f010a43):
    """
    XPrimitive2DRenderer interface.
    
    This interface allows to convert from a sequence of XPrimitive2Ds to a XBitmap

    See Also:
        `API XPrimitive2DRenderer <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1graphic_1_1XPrimitive2DRenderer.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.graphic.XPrimitive2DRenderer']

    def rasterize(self, Primitive2DSequence: 'typing.Tuple[XPrimitive2D_d5730c6d, ...]', aViewInformationSequence: 'typing.Tuple[PropertyValue_c9610c73, ...]', DPIX: int, DPIY: int, Range: 'RealRectangle2D_d9b0e03', MaximumQuadraticPixels: int) -> 'XBitmap_b1b70b7b':
        """
        return rasterized version of given XPrimitive2D
        
        0
        
        is given, a horizontal default resolution of 72 DPI is used.
        
        0
        
        is given, a vertical default resolution of 72 DPI is used.
        """

