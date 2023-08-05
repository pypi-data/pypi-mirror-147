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
# Namespace: com.sun.star.embed
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..awt.key_event import KeyEvent as KeyEvent_7a78097f
    from ..awt.rectangle import Rectangle as Rectangle_84b109e9

class XInplaceObject(XInterface_8f010a43):
    """
    represents common functionality for inplace embedded objects.

    See Also:
        `API XInplaceObject <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1embed_1_1XInplaceObject.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.embed.XInplaceObject']

    def enableModeless(self, bEnable: bool) -> None:
        """
        enables or disables modeless dialogs of the object.
        
        In case container wants to show a modal dialog it should disable modeless of embedded object dialogs with this call. Later the same call can be used to enable it.

        Raises:
            com.sun.star.embed.WrongStateException: ``WrongStateException``
            com.sun.star.uno.Exception: ``Exception``
        """
    def setObjectRectangles(self, aPosRect: 'Rectangle_84b109e9', aClipRect: 'Rectangle_84b109e9') -> None:
        """
        sets the visible part of the inplace object.
        
        Both rectangles are provided in object's parent window coordinates in pixels. The intersection of rectangles specifies the visible part of the object. In case the position window has a size that is different from object's visual area size, the object should either scale or deactivate.
        
        The method must activate object repainting.

        Raises:
            com.sun.star.embed.WrongStateException: ``WrongStateException``
            com.sun.star.uno.Exception: ``Exception``
        """
    def translateAccelerators(self, aKeys: 'typing.Tuple[KeyEvent_7a78097f, ...]') -> None:
        """
        provides accelerator table the container wants to use during inplace editing.

        Raises:
            com.sun.star.embed.WrongStateException: ``WrongStateException``
        """

