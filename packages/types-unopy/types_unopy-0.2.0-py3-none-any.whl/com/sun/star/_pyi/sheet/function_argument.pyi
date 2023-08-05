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
# Namespace: com.sun.star.sheet
# Libre Office Version: 7.3
from typing_extensions import Literal
import typing


class FunctionArgument(object):
    """
    Struct Class

    contains the description of a single argument within a spreadsheet function.

    See Also:
        `API FunctionArgument <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1sheet_1_1FunctionArgument.html>`_
    """
    typeName: Literal['com.sun.star.sheet.FunctionArgument']

    def __init__(self, Name: typing.Optional[str] = ..., Description: typing.Optional[str] = ..., IsOptional: typing.Optional[bool] = ...) -> None:
        """
        Constructor

        Arguments:
            Name (str, optional): Name value.
            Description (str, optional): Description value.
            IsOptional (bool, optional): IsOptional value.
        """


    @property
    def Name(self) -> str:
        """
        the name of the argument.
        """


    @property
    def Description(self) -> str:
        """
        a description of the argument.
        """


    @property
    def IsOptional(self) -> bool:
        """
        determines whether the argument is optional.
        """


