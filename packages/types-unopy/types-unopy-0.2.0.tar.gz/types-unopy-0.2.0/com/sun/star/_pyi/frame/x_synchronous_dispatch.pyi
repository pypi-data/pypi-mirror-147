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
# Namespace: com.sun.star.frame
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..beans.property_value import PropertyValue as PropertyValue_c9610c73
    from ..util.url import URL as URL_57ad07b9

class XSynchronousDispatch(XInterface_8f010a43):
    """
    additional interfaces for dispatch objects: allow to execute with return value
    
    **since**
    
        OOo 2.0

    See Also:
        `API XSynchronousDispatch <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XSynchronousDispatch.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.frame.XSynchronousDispatch']

    def dispatchWithReturnValue(self, URL: 'URL_57ad07b9', Arguments: 'typing.Tuple[PropertyValue_c9610c73, ...]') -> object:
        """
        dispatches a URL synchronously and offers a return values
        
        After getting a dispatch object as a result of a queryDispatch call, this interface can be used to dispatch the URL synchronously and with a return value.
        """

