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
# Namespace: com.sun.star.io
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from .x_data_transfer_event_listener import XDataTransferEventListener as XDataTransferEventListener_54d6103f
    from .x_output_stream import XOutputStream as XOutputStream_a4e00b35
    from ..lang.x_component import XComponent as XComponent_98dc0ab5

class XDataExporter(XInterface_8f010a43):
    """
    makes it possible to export data from a component into a data sink.
    
    Exporter objects are registered for specific components and data types.

    See Also:
        `API XDataExporter <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1io_1_1XDataExporter.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.io.XDataExporter']

    def cancel(self) -> None:
        """
        cancels the export process.
        """
    def exportData(self, aOutputStream: 'XOutputStream_a4e00b35', Component: 'XComponent_98dc0ab5', aListener: 'XDataTransferEventListener_54d6103f') -> None:
        """
        exports data for a component into an output stream.
        """

