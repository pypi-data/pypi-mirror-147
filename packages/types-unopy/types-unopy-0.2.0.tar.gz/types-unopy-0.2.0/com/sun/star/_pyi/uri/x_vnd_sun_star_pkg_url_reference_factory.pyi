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
# Namespace: com.sun.star.uri
from typing_extensions import Literal
import typing
from abc import ABC
if typing.TYPE_CHECKING:
    from .x_uri_reference import XUriReference as XUriReference_afc30b6f

class XVndSunStarPkgUrlReferenceFactory(ABC):
    """
    creates “vnd.sun.star.pkg” URL references.
    
    **since**
    
        OOo 2.0

    See Also:
        `API XVndSunStarPkgUrlReferenceFactory <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1uri_1_1XVndSunStarPkgUrlReferenceFactory.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.uri.XVndSunStarPkgUrlReferenceFactory']

    def createVndSunStarPkgUrlReference(self, authority: 'XUriReference_afc30b6f') -> 'XUriReference_afc30b6f':
        """
        creates a new “vnd.sun.star.pkg” URL reference.
        
        The returned URL reference has the given authority, an empty path, and no fragment.
        """

