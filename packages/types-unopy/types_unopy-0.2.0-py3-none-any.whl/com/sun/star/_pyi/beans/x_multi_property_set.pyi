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
# Namespace: com.sun.star.beans
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .x_properties_change_listener import XPropertiesChangeListener as XPropertiesChangeListener_7a7d1122
    from .x_property_set_info import XPropertySetInfo as XPropertySetInfo_efa90d86

class XMultiPropertySet(XInterface_8f010a43):
    """
    provides access to multiple properties with a single call.

    See Also:
        `API XMultiPropertySet <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1beans_1_1XMultiPropertySet.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.beans.XMultiPropertySet']

    def addPropertiesChangeListener(self, aPropertyNames: 'typing.Tuple[str, ...]', xListener: 'XPropertiesChangeListener_7a7d1122') -> None:
        """
        adds an XPropertiesChangeListener to the specified property with the specified names.
        
        The implementation can ignore the names of the properties and fire the event on all properties.
        
        It is suggested to allow multiple registration of the same listener, thus for each time a listener is added, it has to be removed.
        """
    def firePropertiesChangeEvent(self, aPropertyNames: 'typing.Tuple[str, ...]', xListener: 'XPropertiesChangeListener_7a7d1122') -> None:
        """
        fires a sequence of PropertyChangeEvents to the specified listener.
        """
    def getPropertySetInfo(self) -> 'XPropertySetInfo_efa90d86':
        """
        """
    def getPropertyValues(self, aPropertyNames: 'typing.Tuple[str, ...]') -> 'typing.Tuple[object, ...]':
        """
        The order of the values in the returned sequence will be the same as the order of the names in the argument.
        """
    def removePropertiesChangeListener(self, xListener: 'XPropertiesChangeListener_7a7d1122') -> None:
        """
        removes an XPropertiesChangeListener from the listener list.
        
        It is a \"noop\" if the listener is not registered.
        
        It is suggested to allow multiple registration of the same listener, thus for each time a listener is added, it has to be removed.
        """
    def setPropertyValues(self, aPropertyNames: 'typing.Tuple[str, ...]', aValues: 'typing.Tuple[object, ...]') -> None:
        """
        sets the values to the properties with the specified names.
        
        The values of the properties must change before the bound events are fired. The values of the constrained properties should change after the vetoable events are fired and only if no exception occurred. Unknown properties are ignored.

        Raises:
            com.sun.star.beans.PropertyVetoException: ``PropertyVetoException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
            com.sun.star.lang.WrappedTargetException: ``WrappedTargetException``
        """

