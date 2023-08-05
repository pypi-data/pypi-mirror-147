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
# Namespace: com.sun.star.xml.sax
from typing_extensions import Literal
from ...uno.x_interface import XInterface as XInterface_8f010a43

class XAttributeList(XInterface_8f010a43):
    """
    specifies an element's attributes.
    
    This interface describes a name-type-value triple which describes a single attribute of a tag. Implementors are encouraged to implement the com.sun.star.util.XCloneable interface also to allow the user to make a copy of the instance.
    
    This interface is a poor IDL version of the Java interface org.xml.sax.AttributeList. For example in getValueByName, it does not allow to distinguish a missing value (for which the Java interface returns null) from an empty string value.

    See Also:
        `API XAttributeList <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1xml_1_1sax_1_1XAttributeList.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.xml.sax.XAttributeList']

    def getLength(self) -> int:
        """
        """
    def getNameByIndex(self, i: int) -> str:
        """
        """
    def getTypeByIndex(self, i: int) -> str:
        """
        """
    def getTypeByName(self, aName: str) -> str:
        """
        """
    def getValueByIndex(self, i: int) -> str:
        """
        """
    def getValueByName(self, aName: str) -> str:
        """
        """

