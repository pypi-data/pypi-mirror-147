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
# Exception Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.reflection
# Libre Office Version: 7.3
from typing_extensions import Literal
import typing
from ..uno.exception import Exception as Exception_85530a09
from ..uno.x_interface import XInterface as XInterface_8f010a43

class InvalidTypeNameException(Exception_85530a09):
    """
    Exception Class

    thrown in case that a certain type name does exist, but does not meet some other criteria.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API InvalidTypeNameException <https://api.libreoffice.org/docs/idl/ref/exceptioncom_1_1sun_1_1star_1_1reflection_1_1InvalidTypeNameException.html>`_
    """

    typeName: Literal['com.sun.star.reflection.InvalidTypeNameException']

    def __init__(self, Message: typing.Optional[str] = ..., Context: typing.Optional[XInterface_8f010a43] = ...) -> None:
        """
        Constructor

        Arguments:
            Message (str, optional): Message value.
            Context (XInterface, optional): Context value.
        """

__all__ = ['InvalidTypeNameException']

