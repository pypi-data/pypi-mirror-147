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
# Namespace: com.sun.star.sheet
from typing_extensions import Literal
import typing
from ..lang.x_event_listener import XEventListener as XEventListener_c7230c4a
if typing.TYPE_CHECKING:
    from .activation_event import ActivationEvent as ActivationEvent_e2fc0d35

class XActivationEventListener(XEventListener_c7230c4a):
    """
    makes it possible to receive events when the active spreadsheet changes.
    
    **since**
    
        OOo 2.0

    See Also:
        `API XActivationEventListener <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1sheet_1_1XActivationEventListener.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.sheet.XActivationEventListener']

    def activeSpreadsheetChanged(self, aEvent: 'ActivationEvent_e2fc0d35') -> None:
        """
        is called whenever data or a selection changed.
        
        This interface must be implemented by components that wish to get notified of changes of the active Spreadsheet. They can be registered at an XSpreadsheetViewEventProvider component.
        
        **since**
        
            OOo 2.0
        """

