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
from ..lang.x_event_listener import XEventListener as XEventListener_c7230c4a
if typing.TYPE_CHECKING:
    from .x_frame_loader import XFrameLoader as XFrameLoader_ba3a0bad

class XLoadEventListener(XEventListener_c7230c4a):
    """
    is used to receive callbacks from an asynchronous frame loader.

    See Also:
        `API XLoadEventListener <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XLoadEventListener.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.frame.XLoadEventListener']

    def loadCancelled(self, Loader: 'XFrameLoader_ba3a0bad') -> None:
        """
        is called when a frame load is canceled or failed.
        """
    def loadFinished(self, Loader: 'XFrameLoader_ba3a0bad') -> None:
        """
        is called when a new component is loaded into a frame successfully.
        """

