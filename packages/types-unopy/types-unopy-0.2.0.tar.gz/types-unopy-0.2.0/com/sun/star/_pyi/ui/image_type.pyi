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
# Namespace: com.sun.star.ui
from typing_extensions import Literal


class ImageType:
    """
    Const Class

    Determine the image set of an image manager.
    
    The constants describe bits in a bit field which determine the current image set of an image manager.
    
    **since**
    
        OOo 2.0

    See Also:
        `API ImageType <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1ui_1_1ImageType.html>`_
    """
    SIZE_DEFAULT: Literal[0]
    """
    an image with default size.
    """
    SIZE_LARGE: Literal[1]
    """
    an image with large size.
    """
    SIZE_32: Literal[2]
    """
    an image with size 32.
    
    **since**
    
        LibreOffice 5.3
    """
    COLOR_NORMAL: Literal[0]
    """
    an image with normal colors.
    """
    COLOR_HIGHCONTRAST: Literal[4]
    """
    an image with high contrast colors.
    """

