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
# Namespace: com.sun.star.logging
import typing
from .x_console_handler import XConsoleHandler as XConsoleHandler_fdad0dd8
if typing.TYPE_CHECKING:
    from ..beans.named_value import NamedValue as NamedValue_a37a0af3

class ConsoleHandler(XConsoleHandler_fdad0dd8):
    """
    Service Class

    specifies a component implementing a log handler whose output channel is the processes console.
    
    **since**
    
        OOo 2.3

    See Also:
        `API ConsoleHandler <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1logging_1_1ConsoleHandler.html>`_
    """
    def create(self) -> None:
        """
        creates a ConsoleHandler
        """
    def createWithSettings(self, Settings: 'typing.Tuple[NamedValue_a37a0af3, ...]') -> None:
        """
        creates an instance of the log handler, using generic settings
        
        The following settings are recognized and supported:

        Raises:
            com.sun.star.lang.IllegalArgumentException: ``IllegalArgumentException``
        """


