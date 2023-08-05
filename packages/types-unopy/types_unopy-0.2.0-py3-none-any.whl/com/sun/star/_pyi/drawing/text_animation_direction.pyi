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
# Namespace: com.sun.star.drawing
# Libre Office Version: 7.3
from typing_extensions import Literal
from enum import Enum


class TextAnimationDirection(Enum):
    """
    Enum Class

    

    See Also:
        `API TextAnimationDirection <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1drawing.html#a218f9e180f159784cd3e33cef99bfe86>`_
    """
    DOWN: Literal['DOWN']
    """
    """
    LEFT: Literal['LEFT']
    """
    the connection line leaves the connected object to the left,
    
    The left edge of the text is adjusted to the left edge of the shape.
    
    The text is positioned to the left.
    """
    RIGHT: Literal['RIGHT']
    """
    the connection line leaves the connected object to the right,
    
    The right edge of the text is adjusted to the right edge of the shape.
    
    The text is positioned to the right.
    """
    UP: Literal['UP']
    """
    """

