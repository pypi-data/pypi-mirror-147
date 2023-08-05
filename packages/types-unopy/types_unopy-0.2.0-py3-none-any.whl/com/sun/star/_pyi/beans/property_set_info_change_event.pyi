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
# Struct Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.beans
# Libre Office Version: 7.3
from typing_extensions import Literal
from ..lang.event_object import EventObject as EventObject_a3d70b03
from ..uno.x_interface import XInterface as XInterface_8f010a43
import typing


class PropertySetInfoChangeEvent(EventObject_a3d70b03):
    """
    Struct Class

    gets delivered whenever an XPropertySetInfo is changed.
    
    A PropertySetInfoChangeEvent object is sent to XPropertySetInfoChangeListeners.

    See Also:
        `API PropertySetInfoChangeEvent <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1beans_1_1PropertySetInfoChangeEvent.html>`_
    """
    typeName: Literal['com.sun.star.beans.PropertySetInfoChangeEvent']

    def __init__(self, Source: typing.Optional[XInterface_8f010a43] = ..., Name: typing.Optional[str] = ..., Handle: typing.Optional[int] = ..., Reason: typing.Optional[int] = ...) -> None:
        """
        Constructor

        Arguments:
            Source (XInterface, optional): Source value.
            Name (str, optional): Name value.
            Handle (int, optional): Handle value.
            Reason (int, optional): Reason value.
        """


    @property
    def Name(self) -> str:
        """
        contains the name of the property.
        """


    @property
    def Handle(self) -> int:
        """
        contains the implementation handle for the property.
        
        May be -1 if the implementation has no handle.
        """


    @property
    def Reason(self) -> int:
        """
        contains the reason for the event.
        """


