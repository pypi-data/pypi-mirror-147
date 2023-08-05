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
# Interface Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.chart2
from typing_extensions import Literal
from ..uno.x_interface import XInterface as XInterface_8f010a43

class XScaling(XInterface_8f010a43):
    """

    See Also:
        `API XScaling <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1chart2_1_1XScaling.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.chart2.XScaling']

    def doScaling(self, value: float) -> float:
        """
        Given a numeric value, return the scaled value that conforms to a predefined scaling rule.
        
        For instance, for linear scaling, given a x value, the method may return a y value as defined by y = Ax + B for predefined values of A and B.
        """
    def getInverseScaling(self) -> 'XScaling':
        """
        Get an interface object that conforms to a scaling rule that is the reverse of the original scaling rule.
        """

