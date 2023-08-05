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
# Namespace: com.sun.star.text
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .x_paste_listener import XPasteListener as XPasteListener_c95f0c68

class XPasteBroadcaster(XInterface_8f010a43):
    """
    allows for adding/removing of paste event listeners.
    
    **since**
    
        LibreOffice 6.3

    See Also:
        `API XPasteBroadcaster <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XPasteBroadcaster.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.text.XPasteBroadcaster']

    def addPasteEventListener(self, xListener: 'XPasteListener_c95f0c68') -> None:
        """
        Adds an entry to the list of paste listeners.
        """
    def removePasteEventListener(self, xListener: 'XPasteListener_c95f0c68') -> None:
        """
        Removes an entry to the list of paste listeners.
        """

