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


class ChartLegendPosition(Enum):
    """
    Enum Class

    

    See Also:
        `API ChartLegendPosition <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1chart.html#a65c2b55fdf73cbbf2fdcfef7d305b6c3>`_
    """
    BOTTOM: Literal['BOTTOM']
    """
    displays the chart legend beneath the diagram.
    """
    LEFT: Literal['LEFT']
    """
    displays the chart legend on the left side of the diagram.
    """
    NONE: Literal['NONE']
    """
    error indicators are not displayed.
    
    displays no regression curve.
    
    no chart legend is displayed.
    
    displays no error indicators.
    """
    RIGHT: Literal['RIGHT']
    """
    displays the chart legend on the right side of the diagram.
    """
    TOP: Literal['TOP']
    """
    displays the chart legend above the diagram.
    """

