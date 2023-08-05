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
# Enum Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.style
# Libre Office Version: 7.3
from typing_extensions import Literal
from enum import Enum


class GraphicLocation(Enum):
    """
    Enum Class

    

    See Also:
        `API GraphicLocation <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1style.html#ae71ca73feb713866e85597329dfaec2e>`_
    """
    AREA: Literal['AREA']
    """
    The graphic is scaled to fill the whole surrounding area.
    """
    LEFT_BOTTOM: Literal['LEFT_BOTTOM']
    """
    The graphic is located in the bottom left corner.
    """
    LEFT_MIDDLE: Literal['LEFT_MIDDLE']
    """
    The graphic is located in the middle of the left edge.
    """
    LEFT_TOP: Literal['LEFT_TOP']
    """
    The graphic is located in the top left corner.
    """
    MIDDLE_BOTTOM: Literal['MIDDLE_BOTTOM']
    """
    The graphic is located in the middle of the bottom edge.
    """
    MIDDLE_MIDDLE: Literal['MIDDLE_MIDDLE']
    """
    The graphic is located at the center of the surrounding object.
    """
    MIDDLE_TOP: Literal['MIDDLE_TOP']
    """
    The graphic is located in the middle of the top edge.
    """
    NONE: Literal['NONE']
    """
    No column or page break is applied.
    
    This value specifies that a location is not yet assigned.
    """
    RIGHT_BOTTOM: Literal['RIGHT_BOTTOM']
    """
    The graphic is located in the bottom right corner.
    """
    RIGHT_MIDDLE: Literal['RIGHT_MIDDLE']
    """
    The graphic is located in the middle of the right edge.
    """
    RIGHT_TOP: Literal['RIGHT_TOP']
    """
    The graphic is located in the top right corner.
    """
    TILED: Literal['TILED']
    """
    The graphic is repeatedly spread over the surrounding object like tiles.
    """

