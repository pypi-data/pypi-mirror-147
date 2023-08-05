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
# Namespace: com.sun.star.util
# Libre Office Version: 7.3
from typing_extensions import Literal
from ..lang.event_object import EventObject as EventObject_a3d70b03
from ..uno.x_interface import XInterface as XInterface_8f010a43
import typing


class ModeChangeEvent(EventObject_a3d70b03):
    """
    Struct Class

    allows to veto changes in an object's internal mode.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API ModeChangeEvent <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1util_1_1ModeChangeEvent.html>`_
    """
    typeName: Literal['com.sun.star.util.ModeChangeEvent']

    def __init__(self, Source: typing.Optional[XInterface_8f010a43] = ..., NewMode: typing.Optional[str] = ...) -> None:
        """
        Constructor

        Arguments:
            Source (XInterface, optional): Source value.
            NewMode (str, optional): NewMode value.
        """


    @property
    def NewMode(self) -> str:
        """
        denotes the new internal mode of a component
        
        The semantics of the mode string is to be defined by the component broadcasting this event.
        """


