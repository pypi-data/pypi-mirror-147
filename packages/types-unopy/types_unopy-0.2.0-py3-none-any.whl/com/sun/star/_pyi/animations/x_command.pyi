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
from .x_animation_node import XAnimationNode as XAnimationNode_1cf10eb9

class XCommand(XAnimationNode_1cf10eb9):
    """
    Execution of the XCommand animation node causes the slide show component to call back the application to perform the command.

    See Also:
        `API XCommand <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1animations_1_1XCommand.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.animations.XCommand']

    @property
    def Command(self) -> int:
        """
        This identifies the application specific command.
        
        See documentation of used application for commands.
        """

    @property
    def Parameter(self) -> object:
        """
        The application specific parameter for this command.
        
        See documentation of used application for supported parameters for different commands and target combinations.
        """

    @property
    def Target(self) -> object:
        """
        The application specific target.
        
        See documentation of used application for supported targets.
        """


