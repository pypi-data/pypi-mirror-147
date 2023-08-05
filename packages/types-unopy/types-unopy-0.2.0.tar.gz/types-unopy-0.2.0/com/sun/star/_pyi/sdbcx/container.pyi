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
# Namespace: com.sun.star.sdbcx
from ..container.x_enumeration_access import XEnumerationAccess as XEnumerationAccess_4bac0ffc
from ..container.x_index_access import XIndexAccess as XIndexAccess_f0910d6d
from ..container.x_name_access import XNameAccess as XNameAccess_e2ab0cf6
from .x_append import XAppend as XAppend_847209cc
from .x_data_descriptor_factory import XDataDescriptorFactory as XDataDescriptorFactory_46170fe5
from .x_drop import XDrop as XDrop_71590909
from ..util.x_refreshable import XRefreshable as XRefreshable_b0d60b81

class Container(XEnumerationAccess_4bac0ffc, XIndexAccess_f0910d6d, XNameAccess_e2ab0cf6, XAppend_847209cc, XDataDescriptorFactory_46170fe5, XDrop_71590909, XRefreshable_b0d60b81):
    """
    Service Class

    describes every container which is used for data definition.
    
    Each container must support access to its elements by the element's name or by the element's position.
    
    Simple enumeration must be supported as well.
    
    To reflect the changes with the underlying database, a refresh mechanism needs to be supported.
    
    A container may support the possibility to add new elements or to drop existing elements. Additions are always done by descriptors which define the properties of the new element.

    See Also:
        `API Container <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sdbcx_1_1Container.html>`_
    """


