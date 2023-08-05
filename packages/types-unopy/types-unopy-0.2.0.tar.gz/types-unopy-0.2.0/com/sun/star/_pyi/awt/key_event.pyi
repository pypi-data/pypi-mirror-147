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
# Namespace: com.sun.star.awt
# Libre Office Version: 7.3
from typing_extensions import Literal
from .input_event import InputEvent as InputEvent_8f520a66
from ..uno.x_interface import XInterface as XInterface_8f010a43
import typing


class KeyEvent(InputEvent_8f520a66):
    """
    Struct Class

    specifies a key event.

    See Also:
        `API KeyEvent <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1awt_1_1KeyEvent.html>`_
    """
    typeName: Literal['com.sun.star.awt.KeyEvent']

    def __init__(self, Source: typing.Optional[XInterface_8f010a43] = ..., Modifiers: typing.Optional[int] = ..., KeyCode: typing.Optional[int] = ..., KeyChar: typing.Optional[str] = ..., KeyFunc: typing.Optional[int] = ...) -> None:
        """
        Constructor

        Arguments:
            Source (XInterface, optional): Source value.
            Modifiers (int, optional): Modifiers value.
            KeyCode (int, optional): KeyCode value.
            KeyChar (str, optional): KeyChar value.
            KeyFunc (int, optional): KeyFunc value.
        """


    @property
    def KeyCode(self) -> int:
        """
        contains the integer code representing the key of the event.
        
        This is a constant from the constant group Key.
        """


    @property
    def KeyChar(self) -> str:
        """
        contains the Unicode character generated by this event or 0.
        """


    @property
    def KeyFunc(self) -> int:
        """
        contains the function type of the key event.
        
        This is a constant from the constant group KeyFunction.
        """


