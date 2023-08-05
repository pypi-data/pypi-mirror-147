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
# Namespace: com.sun.star.drawing.framework
from typing_extensions import Literal
import typing
from .x_resource import XResource as XResource_3bcd0f90
if typing.TYPE_CHECKING:
    from ...awt.x_window import XWindow as XWindow_713b0924
    from ...rendering.x_canvas import XCanvas as XCanvas_b19b0b7a

class XPane(XResource_3bcd0f90):
    """
    A pane is an abstraction of a window and is one of the resources managed by the drawing framework.
    
    Apart from the area that displays a view a pane may contain other parts like title, menu, closer button.
    
    The URL prefix of panes is private:resource/floater

    See Also:
        `API XPane <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1drawing_1_1framework_1_1XPane.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.drawing.framework.XPane']

    def getCanvas(self) -> 'XCanvas_b19b0b7a':
        """
        Return the com.sun.star.awt.XCanvas of the pane.
        
        The com.sun.star.rendering.XCanvas object is expected to be associated with the com.sun.star.awt.XWindow object returned by getWindow().
        """
    def getWindow(self) -> 'XWindow_713b0924':
        """
        Return the com.sun.star.awt.XWindow of the pane that is used to display a view.
        """

