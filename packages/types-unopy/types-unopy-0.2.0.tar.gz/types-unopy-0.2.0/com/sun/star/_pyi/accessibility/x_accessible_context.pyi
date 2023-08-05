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
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .x_accessible import XAccessible as XAccessible_1cbc0eb6
    from .x_accessible_relation_set import XAccessibleRelationSet as XAccessibleRelationSet_d8961320
    from .x_accessible_state_set import XAccessibleStateSet as XAccessibleStateSet_a08511e3
    from ..lang.locale import Locale as Locale_70d308fa

class XAccessibleContext(XInterface_8f010a43):
    """
    Implement this interface for exposing various aspects of a class's content.
    
    This interface serves two purposes: On the one hand it gives access to the tree structure in which all accessible objects are organized. Each node in this tree supports this interface. On the other hand it gives access to objects that expose the represented content. That are role, state, name, description, and relations to other objects. Take an OK button of a dialog as an example. Its role is AccessibleRole.BUTTON, its name is \"OK\", and its description is something like \"Accepts all changes made in the dialog\".
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XAccessibleContext <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1accessibility_1_1XAccessibleContext.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.accessibility.XAccessibleContext']

    def getAccessibleChild(self, i: int) -> 'XAccessible_1cbc0eb6':
        """
        Returns the i-th child of this object.
        
        The order in which the children are enumerated is implementation dependent.

        Raises:
            com.sun.star.lang.IndexOutOfBoundsException: ``IndexOutOfBoundsException``
        """
    def getAccessibleChildCount(self) -> int:
        """
        Return the number of children.
        
        Returns the number of accessible children of the object.
        """
    def getAccessibleDescription(self) -> str:
        """
        Returns the object's description.
        
        Returns the object's localized description. The description should complement the more generic descriptions given by an object's role and name.
        """
    def getAccessibleIndexInParent(self) -> int:
        """
        Returns the index of this object in its accessible parent.
        
        If you call getAccessibleChild on the object's parent with the index returned by this function you get a reference to this object.
        """
    def getAccessibleName(self) -> str:
        """
        Return the object's localized name.
        
        See XAccessibleContext.getAccessibleRole()'s documentation for the relation between an object's name and role. Names should be unique, at least between children of the same parent, although the uniqueness is neither enforced nor used inside the API.
        """
    def getAccessibleParent(self) -> 'XAccessible_1cbc0eb6':
        """
        Returns the parent of this object.
        
        This function may be called for every node, including the root node, of the accessible tree.
        """
    def getAccessibleRelationSet(self) -> 'XAccessibleRelationSet_d8961320':
        """
        Returns the set of relations defined for this object.
        
        The returned set of relations is a copy of this object's relation set: changing the returned object does not change this object's relations.
        
        There are two ways to represent an empty list of relations: Return an empty reference or return a valid object that contains an empty list.
        """
    def getAccessibleRole(self) -> int:
        """
        Returns the role of this object.
        
        The role is a generic description of an objects function. The relation between role and name is similar to the relation between class and object.
        """
    def getAccessibleStateSet(self) -> 'XAccessibleStateSet_a08511e3':
        """
        Returns the set of states that are currently active for this object.
        
        The returned state set is a copy: Changing the returned state set will not be reflected by changing the object's set of states. See the documentation of XAccessibleStateSet for a description of the individual states.
        """
    def getLocale(self) -> 'Locale_70d308fa':
        """
        Returns the locale of the component.
        
        This locale is used for example to determine the language to use for the name and description texts.

        Raises:
            IllegalAccessibleComponentStateException: ``IllegalAccessibleComponentStateException``
        """

