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
# Namespace: com.sun.star.animations
from typing_extensions import Literal
from .x_animate import XAnimate as XAnimate_ca680c52

class XAnimateTransform(XAnimate_ca680c52):
    """
    animates a transformation attribute on a target element, thereby allowing animations to control translation, scaling, rotation and/or skewing.
    
    The member XAnimate.Attributes contains a short from AnimationTransformType.
    
    Depending on the value in XAnimate.Attributes, the members XAnimate.From, XAnimate.To, XAnimate.By or XAnimate.Values contain the following

    See Also:
        `API XAnimateTransform <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1animations_1_1XAnimateTransform.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.animations.XAnimateTransform']

    @property
    def TransformType(self) -> int:
        """
        """


