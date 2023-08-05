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
# Namespace: com.sun.star.configuration.backend
from typing_extensions import Literal
from ...uno.x_interface import XInterface as XInterface_8f010a43

class XBackendEntities(XInterface_8f010a43):
    """
    Provides functionality relating to common and supported entities for a configuration data backend.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API XBackendEntities <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1configuration_1_1backend_1_1XBackendEntities.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.configuration.backend.XBackendEntities']

    def getAdminEntity(self) -> str:
        """
        provides the entity id of an entity for general administrative access.
        
        The admin entity is an entity that should be used to read and manage configuration data that applies to all entities within the backend.
        """
    def getOwnerEntity(self) -> str:
        """
        provides the entity id of the owner entity of the backend.
        
        The owner entity is the default entity for the backend. For normal configuration data access the owner entity should always be used.
        """
    def isEqualEntity(self, aEntity: str, aOtherEntity: str) -> bool:
        """
        determines, if two given entity ids denote the same entity.

        Raises:
            BackendAccessException: ``BackendAccessException``
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """
    def supportsEntity(self, aEntity: str) -> bool:
        """
        determines, if a given entity id exists in this backend.

        Raises:
            BackendAccessException: ``BackendAccessException``
        """

