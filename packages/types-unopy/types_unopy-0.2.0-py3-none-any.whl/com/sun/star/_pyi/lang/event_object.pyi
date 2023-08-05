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
# Namespace: com.sun.star.lang
# Libre Office Version: 7.3
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43


class EventObject(object):
    """
    Struct Class

    specifies the base for all event objects and identifies the source of the event.

    See Also:
        `API EventObject <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1lang_1_1EventObject.html>`_
    """
    typeName: Literal['com.sun.star.lang.EventObject']

    def __init__(self, Source: typing.Optional[XInterface_8f010a43] = ...) -> None:
        """
        Constructor

        Arguments:
            Source (XInterface, optional): Source value.
        """


    @property
    def Source(self) -> XInterface_8f010a43:
        """
        refers to the object that fired the event.
        """


