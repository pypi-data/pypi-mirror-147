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
# Namespace: com.sun.star.util
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .x_close_listener import XCloseListener as XCloseListener_c8a60c5a

class XCloseBroadcaster(XInterface_8f010a43):
    """
    broadcasts each tried closing of an object to all interest listener
    
    The called object for closing must post the closing events immediately and before any internal cancel operations will be started. If a listener disagree with that it should throw a CloseVetoException and called function XCloseable.close() must be broken immediately. It's not allowed to catch it inside the close() request. If no listener nor internal processes hinder the object on closing all listeners get a notification about real closing.

    See Also:
        `API XCloseBroadcaster <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1util_1_1XCloseBroadcaster.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.util.XCloseBroadcaster']

    def addCloseListener(self, Listener: 'XCloseListener_c8a60c5a') -> None:
        """
        adds the specified listener to receive or have a veto for \"close\" events
        """
    def removeCloseListener(self, Listener: 'XCloseListener_c8a60c5a') -> None:
        """
        removes the specified listener
        """

