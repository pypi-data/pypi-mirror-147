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
import typing


class DateTime(object):
    """
    Struct Class

    represents a combined date+time value.
    
    **since**
    
        LibreOffice 4.1

    See Also:
        `API DateTime <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1util_1_1DateTime.html>`_
    """
    typeName: Literal['com.sun.star.util.DateTime']

    def __init__(self, NanoSeconds: typing.Optional[int] = ..., Seconds: typing.Optional[int] = ..., Minutes: typing.Optional[int] = ..., Hours: typing.Optional[int] = ..., Day: typing.Optional[int] = ..., Month: typing.Optional[int] = ..., Year: typing.Optional[int] = ..., IsUTC: typing.Optional[bool] = ...) -> None:
        """
        Constructor

        Arguments:
            NanoSeconds (int, optional): NanoSeconds value.
            Seconds (int, optional): Seconds value.
            Minutes (int, optional): Minutes value.
            Hours (int, optional): Hours value.
            Day (int, optional): Day value.
            Month (int, optional): Month value.
            Year (int, optional): Year value.
            IsUTC (bool, optional): IsUTC value.
        """


    @property
    def NanoSeconds(self) -> int:
        """
        contains the nanoseconds (0 - 999 999 999).
        """


    @property
    def Seconds(self) -> int:
        """
        contains the seconds (0-59).
        """


    @property
    def Minutes(self) -> int:
        """
        contains the minutes (0-59).
        """


    @property
    def Hours(self) -> int:
        """
        contains the hour (0-23).
        """


    @property
    def Day(self) -> int:
        """
        is the day of month (1-31 or 0 for a void date).
        """


    @property
    def Month(self) -> int:
        """
        is the month of year (1-12 or 0 for a void date).
        """


    @property
    def Year(self) -> int:
        """
        is the year.
        """


    @property
    def IsUTC(self) -> bool:
        """
        true: time zone is UTC false: unknown time zone.
        
        **since**
        
            LibreOffice 4.1
        """


