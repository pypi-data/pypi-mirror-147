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
# Namespace: com.sun.star.sheet
from ..container.x_enumeration_access import XEnumerationAccess as XEnumerationAccess_4bac0ffc
from ..container.x_index_access import XIndexAccess as XIndexAccess_f0910d6d
from ..document.x_action_lockable import XActionLockable as XActionLockable_cb30e3a
from .x_named_ranges import XNamedRanges as XNamedRanges_bb030bbe

class NamedRanges(XEnumerationAccess_4bac0ffc, XIndexAccess_f0910d6d, XActionLockable_cb30e3a, XNamedRanges_bb030bbe):
    """
    Service Class

    represents a collection of named ranges in a spreadsheet document.
    
    In fact a named range is a named formula expression. A cell range address is one possible content of a named range.
    
    **since**
    
        OOo 3.0

    See Also:
        `API NamedRanges <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sheet_1_1NamedRanges.html>`_
    """


