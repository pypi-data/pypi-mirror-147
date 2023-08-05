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
# Namespace: com.sun.star.form
from typing_extensions import Literal
import typing
from ..lang.x_event_listener import XEventListener as XEventListener_c7230c4a
if typing.TYPE_CHECKING:
    from ..lang.event_object import EventObject as EventObject_a3d70b03

class XRestoreListener(XEventListener_c7230c4a):
    """
    receives notifications about data being restored.
    
    Such a notification is typically sent when the user cancels updating the current record of a database form without saving the data. After restoring, the user operates on the original data.
    
    Please do not use anymore, this interface is deprecated, and superseded by functionality from the com.sun.star.form.component.DataForm and com.sun.star.sdb.RowSet services
    
    .. deprecated::
    
        Class is deprecated.

    See Also:
        `API XRestoreListener <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1form_1_1XRestoreListener.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.form.XRestoreListener']

    def restored(self, aEvent: 'EventObject_a3d70b03') -> None:
        """
        is invoked when a modified record has been restored
        """

