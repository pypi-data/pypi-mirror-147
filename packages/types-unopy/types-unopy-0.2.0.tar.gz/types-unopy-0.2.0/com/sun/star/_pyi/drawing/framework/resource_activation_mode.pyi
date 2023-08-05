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
# Namespace: com.sun.star.drawing.framework
# Libre Office Version: 7.3
from typing_extensions import Literal
from enum import Enum


class ResourceActivationMode(Enum):
    """
    Enum Class

    

    See Also:
        `API ResourceActivationMode <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1drawing_1_1framework.html#a9b6ee17a97f260847a6fa2df1be8f104>`_
    """
    ADD: Literal['ADD']
    """
    A resource is requested in addition to already existing ones.
    
    This is used for example for panes.
    """
    REPLACE: Literal['REPLACE']
    """
    A resource is requested to replace an already existing one of the same class.
    
    This is used for example for views.
    """

