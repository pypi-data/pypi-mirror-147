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
from ..lang.x_event_listener import XEventListener as XEventListener_c7230c4a
if typing.TYPE_CHECKING:
    from .mode_change_event import ModeChangeEvent as ModeChangeEvent_d4140c93

class XModeChangeApproveListener(XEventListener_c7230c4a):
    """
    allows to veto changes in an object's internal mode.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XModeChangeApproveListener <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1util_1_1XModeChangeApproveListener.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.util.XModeChangeApproveListener']

    def approveModeChange(self, rSource: 'ModeChangeEvent_d4140c93') -> None:
        """
        indicates that the mode of the broadcasting component is about to change.
        
        The ModeChangeEvent.NewMode indicates the new mode which is to be set on the component

        Raises:
            VetoException: ``VetoException``
        """

