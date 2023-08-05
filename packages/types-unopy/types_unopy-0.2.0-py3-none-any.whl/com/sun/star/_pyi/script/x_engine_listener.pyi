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
# Namespace: com.sun.star.script
from typing_extensions import Literal
import typing
from ..lang.x_event_listener import XEventListener as XEventListener_c7230c4a
if typing.TYPE_CHECKING:
    from ..lang.event_object import EventObject as EventObject_a3d70b03
    from .finish_engine_event import FinishEngineEvent as FinishEngineEvent_d540e56
    from .interrupt_engine_event import InterruptEngineEvent as InterruptEngineEvent_3e1d0fc2

class XEngineListener(XEventListener_c7230c4a):
    """
    makes it possible to receive events from a scripting engine.
    
    .. deprecated::
    
        Class is deprecated.

    See Also:
        `API XEngineListener <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1script_1_1XEngineListener.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.script.XEngineListener']

    def finished(self, Evt: 'FinishEngineEvent_d540e56') -> None:
        """
        gets fired when the script execution has finished.
        """
    def interrupt(self, Evt: 'InterruptEngineEvent_3e1d0fc2') -> None:
        """
        gets fired when an interrupt occurs during the script execution.
        
        If you call the method, the execution stops. So in this situation, the stack and variable values are still available by using the appropriate XDebugging methods.
        """
    def running(self, Evt: 'EventObject_a3d70b03') -> None:
        """
        gets fired when the script gets into execution state.
        """

