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
    from .all_event_object import AllEventObject as AllEventObject_e2c20d0f

class XAllListener(XEventListener_c7230c4a):
    """
    specifies a listener combining all methods of a listener interface in a single generic call.
    
    Without any output parameters, it is possible to adapt any interface if the XAllListenerAdapterService can generate an adapter.

    See Also:
        `API XAllListener <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1script_1_1XAllListener.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.script.XAllListener']

    def approveFiring(self, aEvent: 'AllEventObject_e2c20d0f') -> object:
        """
        gets called when a \"vetoable event\" occurs at the object.
        
        That happens when the listener method raises an exception, or has a return value declared.

        Raises:
            com.sun.star.reflection.InvocationTargetException: ``InvocationTargetException``
        """
    def firing(self, iaEvent: 'AllEventObject_e2c20d0f') -> None:
        """
        gets called when an event occurs at the object.
        """

