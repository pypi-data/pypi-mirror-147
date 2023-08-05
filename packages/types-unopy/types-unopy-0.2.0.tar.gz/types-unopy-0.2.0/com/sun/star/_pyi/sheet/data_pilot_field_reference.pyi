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


class DataPilotFieldReference(object):
    """
    Struct Class

    controls how a data pilot field's results are shown in relation to a selected reference result.

    See Also:
        `API DataPilotFieldReference <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1sheet_1_1DataPilotFieldReference.html>`_
    """
    typeName: Literal['com.sun.star.sheet.DataPilotFieldReference']

    def __init__(self, ReferenceType: typing.Optional[int] = ..., ReferenceField: typing.Optional[str] = ..., ReferenceItemType: typing.Optional[int] = ..., ReferenceItemName: typing.Optional[str] = ...) -> None:
        """
        Constructor

        Arguments:
            ReferenceType (int, optional): ReferenceType value.
            ReferenceField (str, optional): ReferenceField value.
            ReferenceItemType (int, optional): ReferenceItemType value.
            ReferenceItemName (str, optional): ReferenceItemName value.
        """


    @property
    def ReferenceType(self) -> int:
        """
        contains the type of the reference.
        """


    @property
    def ReferenceField(self) -> str:
        """
        contains the reference field
        """


    @property
    def ReferenceItemType(self) -> int:
        """
        selects between a named reference item and using the previous or next item for each item from the reference field.
        """


    @property
    def ReferenceItemName(self) -> str:
        """
        contains the name of the reference item, when the DataPilotFieldReference.ReferenceItemType is NAMED otherwise is empty
        """


