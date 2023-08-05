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
# Namespace: com.sun.star.container
from typing_extensions import Literal
from .x_element_access import XElementAccess as XElementAccess_cd60e3f

class XMap(XElementAccess_cd60e3f):
    """
    describes a map between keys and values.
    
    Keys in the map are unique, and each key maps to exactly one value.
    
    Locating elements in the map, both values and keys, requires a notion of equality of two objects. In conformance with the UNO type system, two values are said to be equal if and only if they have the same type, and both denote the same element of this type's value set.

    See Also:
        `API XMap <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1container_1_1XMap.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.container.XMap']

    def clear(self) -> None:
        """
        clears the map, removing all key-value pairs from it.

        Raises:
            com.sun.star.lang.NoSupportException: ``NoSupportException``
        """
    def containsKey(self, Key: object) -> bool:
        """
        determines whether a mapping for he given key exists in the map

        Raises:
            com.sun.star.beans.IllegalTypeException: ``IllegalTypeException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    def containsValue(self, Value: object) -> bool:
        """
        determines whether the map contains a mapping to a given value.

        Raises:
            com.sun.star.beans.IllegalTypeException: ``IllegalTypeException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    def get(self, Key: object) -> object:
        """
        gets the value to which a given key maps.

        Raises:
            com.sun.star.beans.IllegalTypeException: ``IllegalTypeException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
            com.sun.star.container.NoSuchElementException: ``NoSuchElementException``
        """
    def put(self, Key: object, Value: object) -> object:
        """
        associates a given key with a given value
        
        If the map already contains a mapping for the given key, then the old value is replaced by the given new value.

        Raises:
            com.sun.star.lang.NoSupportException: ``NoSupportException``
            com.sun.star.beans.IllegalTypeException: ``IllegalTypeException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    def remove(self, Key: object) -> object:
        """
        removes a key-value mapping, given by key, from the map.

        Raises:
            com.sun.star.lang.NoSupportException: ``NoSupportException``
            com.sun.star.beans.IllegalTypeException: ``IllegalTypeException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
            com.sun.star.container.NoSuchElementException: ``NoSuchElementException``
        """
    @property
    def KeyType(self) -> object:
        """
        denotes the type of the keys in the map.
        
        Implementations are free to accept any supertype of KeyType as keys.
        """

    @property
    def ValueType(self) -> object:
        """
        denotes the type of the values in the map.
        
        Implementations are free to accept any supertype of the ValueType as values.
        """


