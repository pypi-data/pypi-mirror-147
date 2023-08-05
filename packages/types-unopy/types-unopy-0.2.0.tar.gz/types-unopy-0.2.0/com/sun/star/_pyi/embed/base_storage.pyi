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
# Namespace: com.sun.star.embed
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from .x_storage import XStorage as XStorage_8e460a32

class BaseStorage(XPropertySet_bc180bfa, XStorage_8e460a32):
    """
    Service Class

    This is a service that allows to get access to a storage hierarchy.

    See Also:
        `API BaseStorage <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1embed_1_1BaseStorage.html>`_
    """
    @property
    def OpenMode(self) -> int:
        """
        allows to get the mode the storage is opened in.
        
        Can be a combination of values from ElementModes.
        """
    @property
    def URL(self) -> str:
        """
        allows to retrieve URL the storage is based on.
        """


