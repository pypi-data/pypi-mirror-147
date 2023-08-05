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
# Namespace: com.sun.star.script.browse
from typing_extensions import Literal
import typing
from ...uno.x_interface import XInterface as XInterface_8f010a43

class XBrowseNode(XInterface_8f010a43):
    """
    This interface represents a node in the hierarchy used to browse available scripts.
    
    Objects implementing this interface are expected to also implement com.sun.star.beans.XPropertySet and, optionally, com.sun.star.script.XInvocation (see the Developer's Guide for more details).

    See Also:
        `API XBrowseNode <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1script_1_1browse_1_1XBrowseNode.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.script.browse.XBrowseNode']

    def getChildNodes(self) -> 'typing.Tuple[XBrowseNode, ...]':
        """
        Get the children of this node.
        """
    def getName(self) -> str:
        """
        Get the name of the node.
        """
    def getType(self) -> int:
        """
        the type of the node.
        """
    def hasChildNodes(self) -> bool:
        """
        Indicates if this node contains any children.
        """

