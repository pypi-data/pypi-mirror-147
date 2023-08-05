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
# Namespace: com.sun.star.i18n
from typing_extensions import Literal
import typing
from .x_locale_data3 import XLocaleData3 as XLocaleData3_a7ad0a9d
if typing.TYPE_CHECKING:
    from ..lang.locale import Locale as Locale_70d308fa

class XLocaleData4(XLocaleData3_a7ad0a9d):
    """
    Access locale specific data.
    
    Derived from com.sun.star.i18n.XLocaleData3 this provides an additional method to return a sequence of date acceptance patterns for a locale.
    
    **since**
    
        LibreOffice 3.6

    See Also:
        `API XLocaleData4 <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1i18n_1_1XLocaleData4.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.i18n.XLocaleData4']

    def getDateAcceptancePatterns(self, aLocale: 'Locale_70d308fa') -> 'typing.Tuple[str, ...]':
        """
        returns a sequence of date acceptance patterns for a locale
        
        Patterns with input combinations that are accepted as incomplete date input, such as M/D or D.M.
        """

