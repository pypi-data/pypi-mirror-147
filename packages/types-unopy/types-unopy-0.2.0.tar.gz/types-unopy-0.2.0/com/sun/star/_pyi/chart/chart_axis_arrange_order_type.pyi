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
# Enum Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.chart
# Libre Office Version: 7.3
from typing_extensions import Literal
from enum import Enum


class ChartAxisArrangeOrderType(Enum):
    """
    Enum Class

    

    See Also:
        `API ChartAxisArrangeOrderType <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1chart.html#a9c06520c0f143b00b5aaafeb4772dc39>`_
    """
    AUTO: Literal['AUTO']
    """
    The descriptions are arranged automatically.
    """
    SIDE_BY_SIDE: Literal['SIDE_BY_SIDE']
    """
    The descriptions are arranged side by side.
    """
    STAGGER_EVEN: Literal['STAGGER_EVEN']
    """
    The descriptions are alternately put on two lines with the even values out of the normal line.
    """
    STAGGER_ODD: Literal['STAGGER_ODD']
    """
    The descriptions are alternately put on two lines with the odd values out of the normal line.
    """

