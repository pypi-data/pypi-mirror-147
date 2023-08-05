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
# Const Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.i18n
from typing_extensions import Literal


class TextConversionType:
    """
    Const Class

    These constants specify the conversion type to be used with XTextConversion.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API TextConversionType <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1i18n_1_1TextConversionType.html>`_
    """
    TO_HANGUL: Literal[1]
    """
    Conversion from Hanja to Hangul.
    """
    TO_HANJA: Literal[2]
    """
    Conversion from Hangul to Hanja.
    """
    TO_SCHINESE: Literal[3]
    """
    Conversion from Traditional to Simplified Chinese.
    """
    TO_TCHINESE: Literal[4]
    """
    Conversion from Simplified to Traditional Chinese.
    """

