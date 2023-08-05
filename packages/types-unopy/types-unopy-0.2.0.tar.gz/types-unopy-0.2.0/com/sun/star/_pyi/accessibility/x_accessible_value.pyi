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
# Namespace: com.sun.star.accessibility
from typing_extensions import Literal
from ..uno.x_interface import XInterface as XInterface_8f010a43

class XAccessibleValue(XInterface_8f010a43):
    """
    Implement this interface to give access to a single numerical value.
    
    The XAccessibleValue interface represents a single numerical value and should be implemented by any class that supports numerical value like scroll bars and spin boxes. This interface lets you access the value and its upper and lower bounds.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XAccessibleValue <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1accessibility_1_1XAccessibleValue.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.accessibility.XAccessibleValue']

    def getCurrentValue(self) -> object:
        """
        Returns the value of this object as a number.
        
        The exact return type is implementation dependent. Typical types are long and double.
        """
    def getMaximumValue(self) -> object:
        """
        Returns the maximal value that can be represented by this object.
        
        The type of the returned value is implementation dependent. It does not have to be the same type as that returned by getCurrentAccessibleValue().
        """
    def getMinimumIncrement(self) -> object:
        """
        Returns the minimal increment by which the value represented by this object can be adjusted.
        
        The type of the returned value is implementation dependent. It does not have to be the same type as that returned by getCurrentAccessibleValue().
        
        **since**
        
            LibreOffice 7.3
        """
    def getMinimumValue(self) -> object:
        """
        Returns the minimal value that can be represented by this object.
        
        The type of the returned value is implementation dependent. It does not have to be the same type as that returned by getCurrentAccessibleValue().
        """
    def setCurrentValue(self, aNumber: object) -> bool:
        """
        Sets the value of this object to the given number.
        
        The argument is clipped to the valid interval whose upper and lower bounds are returned by the methods getMaximumAccessibleValue() and getMinimumAccessibleValue(), i.e. if it is lower than the minimum value the new value will be the minimum and if it is greater than the maximum then the new value will be the maximum.
        """

