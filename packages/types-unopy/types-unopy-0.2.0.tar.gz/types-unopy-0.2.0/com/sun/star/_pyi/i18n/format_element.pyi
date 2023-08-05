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
# Namespace: com.sun.star.i18n
# Libre Office Version: 7.3
from typing_extensions import Literal
import typing


class FormatElement(object):
    """
    Struct Class

    One number format code and its attributes, returned in a sequence by XLocaleData.getAllFormats().
    
    Contains raw data defined in the XML locale data files.

    See Also:
        `API FormatElement <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1i18n_1_1FormatElement.html>`_
    """
    typeName: Literal['com.sun.star.i18n.FormatElement']

    def __init__(self, formatCode: typing.Optional[str] = ..., formatName: typing.Optional[str] = ..., formatKey: typing.Optional[str] = ..., formatType: typing.Optional[str] = ..., formatUsage: typing.Optional[str] = ..., formatIndex: typing.Optional[int] = ..., isDefault: typing.Optional[bool] = ...) -> None:
        """
        Constructor

        Arguments:
            formatCode (str, optional): formatCode value.
            formatName (str, optional): formatName value.
            formatKey (str, optional): formatKey value.
            formatType (str, optional): formatType value.
            formatUsage (str, optional): formatUsage value.
            formatIndex (int, optional): formatIndex value.
            isDefault (bool, optional): isDefault value.
        """


    @property
    def formatCode(self) -> str:
        """
        The format code, for example, \"YYYY-MM-DD\".
        """


    @property
    def formatName(self) -> str:
        """
        A name or description that is displayed in the number formatter dialog.
        """


    @property
    def formatKey(self) -> str:
        """
        A unique (within one locale) identifier.
        """


    @property
    def formatType(self) -> str:
        """
        Type may be one of \"short\", \"medium\", \"long\".
        """


    @property
    def formatUsage(self) -> str:
        """
        Usage category, for example, \"DATE\" or \"FIXED_NUMBER\", corresponding with KNumberFormatUsage values.
        """


    @property
    def formatIndex(self) -> int:
        """
        The index used by the number formatter, predefined values corresponding with NumberFormatIndex values.
        """


    @property
    def isDefault(self) -> bool:
        """
        If a format code is the default code of a formatType group.
        """


