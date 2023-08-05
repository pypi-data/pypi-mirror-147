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
# Namespace: com.sun.star.xml.dom
from typing_extensions import Literal
import typing
from .x_node import XNode as XNode_83fb09a5
if typing.TYPE_CHECKING:
    from .x_attr import XAttr as XAttr_840309ba
    from .x_node_list import XNodeList as XNodeList_ae540b41

class XElement(XNode_83fb09a5):
    """

    See Also:
        `API XElement <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1xml_1_1dom_1_1XElement.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.xml.dom.XElement']

    def getAttribute(self, name: str) -> str:
        """
        Retrieves an attribute value by name.
        """
    def getAttributeNS(self, namespaceURI: str, localName: str) -> str:
        """
        Retrieves an attribute value by local name and namespace URI.
        """
    def getAttributeNode(self, name: str) -> 'XAttr_840309ba':
        """
        Retrieves an attribute node by name.
        """
    def getAttributeNodeNS(self, namespaceURI: str, localName: str) -> 'XAttr_840309ba':
        """
        Retrieves an Attr node by local name and namespace URI.
        """
    def getElementsByTagName(self, name: str) -> 'XNodeList_ae540b41':
        """
        Returns a NodeList of all descendant Elements with a given tag name, in the order in which they are encountered in a preorder traversal of this Element tree.
        """
    def getElementsByTagNameNS(self, namespaceURI: str, localName: str) -> 'XNodeList_ae540b41':
        """
        Returns a NodeList of all the descendant Elements with a given local name and namespace URI in the order in which they are encountered in a preorder traversal of this Element tree.
        """
    def getTagName(self) -> str:
        """
        The name of the element.
        """
    def hasAttribute(self, name: str) -> bool:
        """
        Returns true when an attribute with a given name is specified on this element or has a default value, false otherwise.
        """
    def hasAttributeNS(self, namespaceURI: str, localName: str) -> bool:
        """
        Returns true when an attribute with a given local name and namespace URI is specified on this element or has a default value, false otherwise.
        """
    def removeAttribute(self, name: str) -> None:
        """
        Removes an attribute by name.
        
        Throws: DOMException - NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly.

        Raises:
            DOMException: ``DOMException``
        """
    def removeAttributeNS(self, namespaceURI: str, localName: str) -> None:
        """
        Removes an attribute by local name and namespace URI.
        
        Throws: DOMException - NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly.

        Raises:
            DOMException: ``DOMException``
        """
    def removeAttributeNode(self, oldAttr: 'XAttr_840309ba') -> 'XAttr_840309ba':
        """
        Removes the specified attribute node.
        
        Throws: DOMException - NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly. NOT_FOUND_ERR: Raised if oldAttr is not an attribute of the element.

        Raises:
            DOMException: ``DOMException``
        """
    def setAttribute(self, name: str, value: str) -> None:
        """
        Adds a new attribute.
        
        Throws: DOMException - INVALID_CHARACTER_ERR: Raised if the specified name contains an illegal character. NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly.

        Raises:
            DOMException: ``DOMException``
        """
    def setAttributeNS(self, namespaceURI: str, qualifiedName: str, value: str) -> None:
        """
        Adds a new attribute.
        
        Throws: DOMException - INVALID_CHARACTER_ERR: Raised if the specified qualified name contains an illegal character, per the XML 1.0 specification . NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly. NAMESPACE_ERR: Raised if the qualifiedName is malformed per the Namespaces in XML specification, if the qualifiedName has a prefix and the namespaceURI is null, if the qualifiedName has a prefix that is \"xml\" and the namespaceURI is different from \" http://www.w3.org/XML/1998/namespace\", or if the qualifiedName, or its prefix, is \"xmlns\" and the namespaceURI is different from \" http://www.w3.org/2000/xmlns/\". NOT_SUPPORTED_ERR: Always thrown if the current document does not support the \"XML\" feature, since namespaces were defined by XML.

        Raises:
            DOMException: ``DOMException``
        """
    def setAttributeNode(self, newAttr: 'XAttr_840309ba') -> 'XAttr_840309ba':
        """
        Adds a new attribute node.
        
        Throws: DOMException - WRONG_DOCUMENT_ERR: Raised if newAttr was created from a different document than the one that created the element. NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly. INUSE_ATTRIBUTE_ERR: Raised if newAttr is already an attribute of another Element object. The DOM user must explicitly clone Attr nodes to re-use them in other elements.

        Raises:
            DOMException: ``DOMException``
        """
    def setAttributeNodeNS(self, newAttr: 'XAttr_840309ba') -> 'XAttr_840309ba':
        """
        Adds a new attribute.
        
        Throws: DOMException - WRONG_DOCUMENT_ERR: Raised if newAttr was created from a different document than the one that created the element. NO_MODIFICATION_ALLOWED_ERR: Raised if this node is readonly. INUSE_ATTRIBUTE_ERR: Raised if newAttr is already an attribute of another Element object. The DOM user must explicitly clone Attr nodes to re-use them in other elements. NOT_SUPPORTED_ERR: Always thrown if the current document does not support the \"XML\" feature, since namespaces were defined by XML.

        Raises:
            DOMException: ``DOMException``
        """

