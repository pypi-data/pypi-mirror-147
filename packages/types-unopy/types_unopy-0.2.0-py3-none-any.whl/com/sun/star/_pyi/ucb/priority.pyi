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
# Namespace: com.sun.star.ucb
# Libre Office Version: 7.3
from typing_extensions import Literal
from enum import Enum


class Priority(Enum):
    """
    Enum Class

    

    See Also:
        `API Priority <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1ucb.html#a315655b1bb5848c063491adffde62b15>`_
    """
    HIGH: Literal['HIGH']
    """
    High priority.
    """
    HIGHEST: Literal['HIGHEST']
    """
    Highest priority.
    """
    LOW: Literal['LOW']
    """
    Low priority.
    """
    LOWEST: Literal['LOWEST']
    """
    Lowest priority.
    """
    NORMAL: Literal['NORMAL']
    """
    Normal priority.
    """

