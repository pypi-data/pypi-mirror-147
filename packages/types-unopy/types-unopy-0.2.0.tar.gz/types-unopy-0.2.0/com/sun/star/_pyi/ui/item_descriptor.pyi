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
# Service Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.ui
import typing
from abc import ABC
if typing.TYPE_CHECKING:
    from ..container.x_index_access import XIndexAccess as XIndexAccess_f0910d6d

class ItemDescriptor(ABC):
    """
    Service Class

    describes a user interface item that is part of a user interface element.
    
    Common examples for such elements are:
    
    No assumption is made about any graphical representation: You could have a menu or a toolbox working with the same item descriptor.
    
    **since**
    
        OOo 2.0

    See Also:
        `API ItemDescriptor <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1ui_1_1ItemDescriptor.html>`_
    """
    @property
    def CommandURL(self) -> str:
        """
        contains the command URL which specifies which action should be accomplished.
        """
    @property
    def HelpURL(self) -> str:
        """
        contains the a URL that points to a help text.
        """
    @property
    def IsVisible(self) -> bool:
        """
        specifies if this item is visible or not.
        
        This property is only valid if the item describes a toolbar or statusbar item.
        """
    @property
    def ItemDescriptorContainer(self) -> 'XIndexAccess_f0910d6d':
        """
        specifies an optional sub container.
        
        This property is valid for menus only. It can be used to define sub menus.
        """
    @property
    def Label(self) -> str:
        """
        the text of the user interface item.
        """
    @property
    def Offset(self) -> int:
        """
        specifies the pixel distance by which the text of the item is shifted on the x-axis.
        
        This property is only valid if the item describes a statusbar item.
        """
    @property
    def Style(self) -> int:
        """
        different styles which influence the appearance of the item and its behavior.
        
        This property is only valid if the item describes a toolbar or statusbar item. See ItemStyle for more information about possible styles.
        """
    @property
    def Type(self) -> int:
        """
        specifies which type this item descriptor belongs to.
        
        See constant definition ItemType.
        """
    @property
    def Width(self) -> int:
        """
        specifies a pixel width for this item inside the user interface element.
        
        This property is only valid if the item describes a toolbar or statusbar item.
        """


