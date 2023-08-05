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
# Namespace: com.sun.star.drawing
import typing
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from ..document.office_document import OfficeDocument as OfficeDocument_fecd0df2
from .x_draw_page_duplicator import XDrawPageDuplicator as XDrawPageDuplicator_37bd0f6e
from .x_draw_pages_supplier import XDrawPagesSupplier as XDrawPagesSupplier_29650f1e
from .x_layer_supplier import XLayerSupplier as XLayerSupplier_f0da0d9d
from .x_master_pages_supplier import XMasterPagesSupplier as XMasterPagesSupplier_49bb0ffc
from ..lang.x_multi_service_factory import XMultiServiceFactory as XMultiServiceFactory_191e0eb6
from ..style.x_style_families_supplier import XStyleFamiliesSupplier as XStyleFamiliesSupplier_4c5a1020
if typing.TYPE_CHECKING:
    from ..awt.rectangle import Rectangle as Rectangle_84b109e9
    from ..i18n.x_forbidden_characters import XForbiddenCharacters as XForbiddenCharacters_df60e2d
    from ..lang.locale import Locale as Locale_70d308fa

class GenericDrawingDocument(OfficeDocument_fecd0df2, XPropertySet_bc180bfa, XDrawPageDuplicator_37bd0f6e, XDrawPagesSupplier_29650f1e, XLayerSupplier_f0da0d9d, XMasterPagesSupplier_49bb0ffc, XMultiServiceFactory_191e0eb6, XStyleFamiliesSupplier_4c5a1020):
    """
    Service Class

    specifies a document which consists of multiple pages with drawings.
    
    Because its function is needed more than once, it's defined as generic one.

    See Also:
        `API GenericDrawingDocument <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1drawing_1_1GenericDrawingDocument.html>`_
    """
    @property
    def CharLocale(self) -> 'Locale_70d308fa':
        """
        contains the identifier of the default locale of the document.
        """
    @property
    def ForbiddenCharacters(self) -> 'XForbiddenCharacters_df60e2d':
        """
        This property gives the XForbiddenCharacters.
        """
    @property
    def TabStop(self) -> int:
        """
        This property specifies the length between the default tab stops inside text in this document in 1/100th mm.
        """
    @property
    def VisibleArea(self) -> 'Rectangle_84b109e9':
        """
        if this document is an OLE client, this is the current visible area in 100th mm
        """


