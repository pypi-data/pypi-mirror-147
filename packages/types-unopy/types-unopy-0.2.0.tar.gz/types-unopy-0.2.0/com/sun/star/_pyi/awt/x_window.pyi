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
from ..lang.x_component import XComponent as XComponent_98dc0ab5
if typing.TYPE_CHECKING:
    from .rectangle import Rectangle as Rectangle_84b109e9
    from .x_focus_listener import XFocusListener as XFocusListener_bb8e0bf2
    from .x_key_listener import XKeyListener as XKeyListener_a4020b1b
    from .x_mouse_listener import XMouseListener as XMouseListener_bc1d0bfb
    from .x_mouse_motion_listener import XMouseMotionListener as XMouseMotionListener_c6a0e71
    from .x_paint_listener import XPaintListener as XPaintListener_bb6d0bee
    from .x_window_listener import XWindowListener as XWindowListener_c8aa0c6a

class XWindow(XComponent_98dc0ab5):
    """
    specifies the basic operations for a window component.
    
    A window is a rectangular region on an output device with its own position, size, and internal coordinate system. A window is used for displaying data. In addition, the window receives events from the user.

    See Also:
        `API XWindow <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XWindow.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.awt.XWindow']

    def addFocusListener(self, xListener: 'XFocusListener_bb8e0bf2') -> None:
        """
        adds a focus listener to the object.
        """
    def addKeyListener(self, xListener: 'XKeyListener_a4020b1b') -> None:
        """
        adds a key listener to the object.
        """
    def addMouseListener(self, xListener: 'XMouseListener_bc1d0bfb') -> None:
        """
        adds a mouse listener to the object.
        """
    def addMouseMotionListener(self, xListener: 'XMouseMotionListener_c6a0e71') -> None:
        """
        adds a mouse motion listener to the object.
        """
    def addPaintListener(self, xListener: 'XPaintListener_bb6d0bee') -> None:
        """
        adds a paint listener to the object.
        """
    def addWindowListener(self, xListener: 'XWindowListener_c8aa0c6a') -> None:
        """
        adds a window listener to the object.
        """
    def getPosSize(self) -> 'Rectangle_84b109e9':
        """
        returns the outer bounds of the window.
        """
    def removeFocusListener(self, xListener: 'XFocusListener_bb8e0bf2') -> None:
        """
        removes the specified focus listener from the listener list.
        """
    def removeKeyListener(self, xListener: 'XKeyListener_a4020b1b') -> None:
        """
        removes the specified key listener from the listener list.
        """
    def removeMouseListener(self, xListener: 'XMouseListener_bc1d0bfb') -> None:
        """
        removes the specified mouse listener from the listener list.
        """
    def removeMouseMotionListener(self, xListener: 'XMouseMotionListener_c6a0e71') -> None:
        """
        removes the specified mouse motion listener from the listener list.
        """
    def removePaintListener(self, xListener: 'XPaintListener_bb6d0bee') -> None:
        """
        removes the specified paint listener from the listener list.
        """
    def removeWindowListener(self, xListener: 'XWindowListener_c8aa0c6a') -> None:
        """
        removes the specified window listener from the listener list.
        """
    def setEnable(self, Enable: bool) -> None:
        """
        enables or disables the window depending on the parameter.
        """
    def setFocus(self) -> None:
        """
        sets the focus to the window.
        """
    def setPosSize(self, X: int, Y: int, Width: int, Height: int, Flags: int) -> None:
        """
        sets the outer bounds of the window.
        """
    def setVisible(self, Visible: bool) -> None:
        """
        shows or hides the window depending on the parameter.
        """

