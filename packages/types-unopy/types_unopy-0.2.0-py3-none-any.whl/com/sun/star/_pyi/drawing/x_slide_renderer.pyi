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
# Namespace: com.sun.star.drawing
from typing_extensions import Literal
import typing
from abc import ABC
if typing.TYPE_CHECKING:
    from ..awt.size import Size as Size_576707ef
    from ..awt.x_bitmap import XBitmap as XBitmap_70cd0909
    from .x_draw_page import XDrawPage as XDrawPage_b07a0b57
    from ..rendering.x_bitmap import XBitmap as XBitmap_b1b70b7b
    from ..rendering.x_canvas import XCanvas as XCanvas_b19b0b7a

class XSlideRenderer(ABC):
    """
    Create preview bitmaps for single slides.

    See Also:
        `API XSlideRenderer <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1drawing_1_1XSlideRenderer.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.drawing.XSlideRenderer']

    def calculatePreviewSize(self, nSlideAspectRatio: float, aMaximumPreviewPixelSize: 'Size_576707ef') -> 'Size_576707ef':
        """
        Return a size that has the given aspect ratio and shares either the width or the height with the given maximum size.
        """
    def createPreview(self, xSlide: 'XDrawPage_b07a0b57', aMaximumPreviewPixelSize: 'Size_576707ef', nSuperSampleFactor: int) -> 'XBitmap_70cd0909':
        """
        Create a preview for the given slide that has the same aspect ratio as the page and is as large as possible but not larger than the specified size.
        
        The reason for not using the given size directly as preview size and thus possibly changing the aspect ratio is that a) a different aspect ratio is not used often, and b) leaving the adaptation of the actual preview size (according to the aspect ratio of the slide) to the slide renderer is more convenient to the caller than having to this himself.
        """
    def createPreviewForCanvas(self, xSlide: 'XDrawPage_b07a0b57', aMaximumPreviewPixelSize: 'Size_576707ef', nSuperSampleFactor: int, xCanvas: 'XCanvas_b19b0b7a') -> 'XBitmap_b1b70b7b':
        """
        Exactly the same functionality as createPreview(), only a different return type: com.sun.star.rendering.XBitmap instead of com.sun.star.awt.XBitmap.
        """

