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
# Namespace: com.sun.star.deployment
from typing_extensions import Literal
import typing
from abc import ABC

class XPackageInformationProvider(ABC):
    """
    Objects implementing this interface provide a URL to the root of an installed package.
    
    **since**
    
        OOo 2.3

    See Also:
        `API XPackageInformationProvider <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1deployment_1_1XPackageInformationProvider.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.deployment.XPackageInformationProvider']

    def getExtensionList(self) -> 'typing.Tuple[typing.Tuple[str, ...], ...]':
        """
        returns a list of all installed extension with their version.
        """
    def getPackageLocation(self, extensionId: str) -> str:
        """
        get Package information for a specific extension.
        """
    def isUpdateAvailable(self, extensionId: str) -> 'typing.Tuple[typing.Tuple[str, ...], ...]':
        """
        check if there are updates available for an extension.
        """

