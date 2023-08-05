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
# Exception Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.configuration.backend
# Libre Office Version: 7.3
from typing_extensions import Literal
from ooo.oenv.env_const import UNO_NONE
import typing
from .backend_setup_exception import BackendSetupException as BackendSetupException_68ae15de
from ...uno.x_interface import XInterface as XInterface_8f010a43

class StratumCreationException(BackendSetupException_68ae15de):
    """
    Exception Class

    is passed to an InteractionHandler when creating a stratum backend fails.
    
    **since**
    
        OOo 2.0

    See Also:
        `API StratumCreationException <https://api.libreoffice.org/docs/idl/ref/exceptioncom_1_1sun_1_1star_1_1configuration_1_1backend_1_1StratumCreationException.html>`_
    """

    typeName: Literal['com.sun.star.configuration.backend.StratumCreationException']

    def __init__(self, Message: typing.Optional[str] = ..., Context: typing.Optional[XInterface_8f010a43] = ..., BackendException: typing.Optional[object] = ..., StratumService: typing.Optional[str] = ..., StratumData: typing.Optional[str] = ...) -> None:
        """
        Constructor

        Arguments:
            Message (str, optional): Message value.
            Context (XInterface, optional): Context value.
            BackendException (object, optional): BackendException value.
            StratumService (str, optional): StratumService value.
            StratumData (str, optional): StratumData value.
        """
    @property
    def StratumService(self) -> str:
        """
        Identifier of the stratum service that could not be created.
        """

    @property
    def StratumData(self) -> str:
        """
        Initialization data passed to the stratum instance.
        """


__all__ = ['StratumCreationException']

