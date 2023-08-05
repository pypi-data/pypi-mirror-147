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
from ..lang.x_component import XComponent as XComponent_98dc0ab5
if typing.TYPE_CHECKING:
    from ..awt.x_window import XWindow as XWindow_713b0924

class XDesktopTask(XComponent_98dc0ab5):
    """
    use XFrame instead of this
    
    .. deprecated::
    
        Class is deprecated.

    See Also:
        `API XDesktopTask <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XDesktopTask.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.frame.XDesktopTask']

    def close(self) -> bool:
        """
        use com.sun.star.util.XCloseable or com.sun.star.lang.XComponent.dispose() instead.
        """
    def initialize(self, TaskWindow: 'XWindow_713b0924') -> None:
        """
        use com.sun.star.lang.XInitialization instead.
        """

