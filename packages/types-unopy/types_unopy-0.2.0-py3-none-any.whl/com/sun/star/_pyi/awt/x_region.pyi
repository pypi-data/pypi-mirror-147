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
# Namespace: com.sun.star.awt
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .rectangle import Rectangle as Rectangle_84b109e9

class XRegion(XInterface_8f010a43):
    """
    manages multiple rectangles which make up a region.

    See Also:
        `API XRegion <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XRegion.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.awt.XRegion']

    def clear(self) -> None:
        """
        makes this region an empty region.
        """
    def excludeRectangle(self, Rect: 'Rectangle_84b109e9') -> None:
        """
        removes the area of the specified rectangle from this region.
        """
    def excludeRegion(self, Region: 'XRegion') -> None:
        """
        removes the area of the specified region from this region.
        """
    def getBounds(self) -> 'Rectangle_84b109e9':
        """
        returns the bounding box of the shape.
        """
    def getRectangles(self) -> 'typing.Tuple[Rectangle_84b109e9, ...]':
        """
        returns all rectangles which are making up this region.
        """
    def intersectRectangle(self, Region: 'Rectangle_84b109e9') -> None:
        """
        intersects the specified rectangle with the current region.
        """
    def intersectRegion(self, Region: 'XRegion') -> None:
        """
        intersects the specified region with the current region.
        """
    def move(self, nHorzMove: int, nVertMove: int) -> None:
        """
        moves this region by the specified horizontal and vertical delta.
        """
    def unionRectangle(self, Rect: 'Rectangle_84b109e9') -> None:
        """
        adds the specified rectangle to this region.
        """
    def unionRegion(self, Region: 'XRegion') -> None:
        """
        adds the specified region to this region.
        """
    def xOrRectangle(self, Rect: 'Rectangle_84b109e9') -> None:
        """
        applies an exclusive-or operation with the specified rectangle to this region.
        """
    def xOrRegion(self, Region: 'XRegion') -> None:
        """
        applies an exclusive-or operation with the specified region to this region.
        """

