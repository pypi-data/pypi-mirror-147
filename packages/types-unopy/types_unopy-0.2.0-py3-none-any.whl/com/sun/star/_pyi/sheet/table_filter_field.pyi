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
from .filter_connection import FilterConnection as FilterConnection_f01f0d97
from .filter_operator import FilterOperator as FilterOperator_d5c60cd3


class TableFilterField(object):
    """
    Struct Class

    describes a single condition in a filter descriptor.

    See Also:
        `API TableFilterField <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1sheet_1_1TableFilterField.html>`_
    """
    typeName: Literal['com.sun.star.sheet.TableFilterField']

    def __init__(self, Connection: typing.Optional[FilterConnection_f01f0d97] = ..., Field: typing.Optional[int] = ..., Operator: typing.Optional[FilterOperator_d5c60cd3] = ..., IsNumeric: typing.Optional[bool] = ..., NumericValue: typing.Optional[float] = ..., StringValue: typing.Optional[str] = ...) -> None:
        """
        Constructor

        Arguments:
            Connection (FilterConnection, optional): Connection value.
            Field (int, optional): Field value.
            Operator (FilterOperator, optional): Operator value.
            IsNumeric (bool, optional): IsNumeric value.
            NumericValue (float, optional): NumericValue value.
            StringValue (str, optional): StringValue value.
        """


    @property
    def Connection(self) -> FilterConnection_f01f0d97:
        """
        specifies how the condition is connected to the previous condition.
        """


    @property
    def Field(self) -> int:
        """
        specifies which field (column) is used for the condition.
        """


    @property
    def Operator(self) -> FilterOperator_d5c60cd3:
        """
        specifies the type of the condition.
        """


    @property
    def IsNumeric(self) -> bool:
        """
        selects whether the TableFilterField.NumericValue or the TableFilterField.StringValue is used.
        """


    @property
    def NumericValue(self) -> float:
        """
        specifies a numeric value for the condition.
        """


    @property
    def StringValue(self) -> str:
        """
        specifies a string value for the condition.
        """


