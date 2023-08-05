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
# Namespace: com.sun.star.configuration.backend
from .x_layer import XLayer as XLayer_4cd50fcb
from ...lang.x_initialization import XInitialization as XInitialization_d46c0cca

class LayerFilter(XLayer_4cd50fcb, XInitialization_d46c0cca):
    """
    Service Class

    provides a filtered version of a configuration data Layer.
    
    A layer filter wraps a source XLayer object and provides access to a filtered version of its data. The data read from the filter usually is produced from the source data by adding and removing elements or modifying values.
    
    **since**
    
        OOo 2.0

    See Also:
        `API LayerFilter <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1configuration_1_1backend_1_1LayerFilter.html>`_
    """


