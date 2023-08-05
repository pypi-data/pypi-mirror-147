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
# Namespace: com.sun.star.gallery
import typing
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from .x_gallery_item import XGalleryItem as XGalleryItem_d5730caf
if typing.TYPE_CHECKING:
    from ..graphic.x_graphic import XGraphic as XGraphic_a4da0afc
    from ..lang.x_component import XComponent as XComponent_98dc0ab5

class GalleryItem(XPropertySet_bc180bfa, XGalleryItem_d5730caf):
    """
    Service Class

    service to get access to the properties of a single Gallery item

    See Also:
        `API GalleryItem <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1gallery_1_1GalleryItem.html>`_
    """
    @property
    def Drawing(self) -> 'XComponent_98dc0ab5':
        """
        the drawing content of the Gallery item
        
        This is an optional property and may not available for every item
        """
    @property
    def GalleryItemType(self) -> int:
        """
        The type of the Gallery item.
        """
    @property
    def Graphic(self) -> 'XGraphic_a4da0afc':
        """
        the graphic content of the Gallery item
        
        This is an optional property and may not available for every item
        """
    @property
    def Thumbnail(self) -> 'XGraphic_a4da0afc':
        """
        the thumbnail of the Gallery item
        
        The thumbnail may be either a pixel or a vector graphic
        """
    @property
    def Title(self) -> str:
        """
        the title of the Gallery item
        """
    @property
    def URL(self) -> str:
        """
        the URL of the Gallery item
        
        The interpretation of the URL depends on the type of the Gallery item. In case of graphic and media items, the URL is a \"real\" URL, in case of drawings it is a private URL
        """


