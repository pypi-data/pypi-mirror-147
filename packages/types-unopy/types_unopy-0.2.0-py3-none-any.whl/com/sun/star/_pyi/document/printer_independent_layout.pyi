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
# Namespace: com.sun.star.document
from typing_extensions import Literal


class PrinterIndependentLayout:
    """
    Const Class

    specifies whether the document printer metric is used.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API PrinterIndependentLayout <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1document_1_1PrinterIndependentLayout.html>`_
    """
    DISABLED: Literal[1]
    """
    use printer-dependent metrics for layout
    """
    LOW_RESOLUTION: Literal[2]
    """
    use printer-independent metrics for layout, assuming a generic 600dpi printer
    """
    ENABLED: Literal[2]
    HIGH_RESOLUTION: Literal[3]
    """
    use printer-independent metrics for layout, assuming a generic high-resolution printer (4800dpi)
    """

