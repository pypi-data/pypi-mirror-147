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
# Namespace: com.sun.star.sdb
# Libre Office Version: 7.3
from typing_extensions import Literal
from ooo.oenv.env_const import UNO_NONE
import typing
from ..task.classified_interaction_request import ClassifiedInteractionRequest as ClassifiedInteractionRequest_9f72121b
from ..uno.x_interface import XInterface as XInterface_8f010a43
from ..task.interaction_classification import InteractionClassification as InteractionClassification_6c4d10e7
from ..container.x_index_access import XIndexAccess as XIndexAccess_f0910d6d
from ..sdbc.x_connection import XConnection as XConnection_a36a0b0c

class ParametersRequest(ClassifiedInteractionRequest_9f72121b):
    """
    Exception Class

    an error specifying the lack of parameters values
    
    Usually thrown if someone tries to execute an SQL statement containing parameters which can't be filled by the executing instance.

    See Also:
        `API ParametersRequest <https://api.libreoffice.org/docs/idl/ref/exceptioncom_1_1sun_1_1star_1_1sdb_1_1ParametersRequest.html>`_
    """

    typeName: Literal['com.sun.star.sdb.ParametersRequest']

    def __init__(self, Message: typing.Optional[str] = ..., Context: typing.Optional[XInterface_8f010a43] = ..., Classification: typing.Optional[InteractionClassification_6c4d10e7] = ..., Parameters: typing.Optional[XIndexAccess_f0910d6d] = ..., Connection: typing.Optional[XConnection_a36a0b0c] = ...) -> None:
        """
        Constructor

        Arguments:
            Message (str, optional): Message value.
            Context (XInterface, optional): Context value.
            Classification (InteractionClassification, optional): Classification value.
            Parameters (XIndexAccess, optional): Parameters value.
            Connection (XConnection, optional): Connection value.
        """
    @property
    def Parameters(self) -> XIndexAccess_f0910d6d:
        """
        is the list of parameters requested.
        
        The objects returned by the com.sun.star.container.XIndexAccess have to be property sets describing the respective parameter. For this, the objects have to support the service com.sun.star.sdbcx.Column.
        """

    @property
    def Connection(self) -> XConnection_a36a0b0c:
        """
        specifies the connection on which the statement is to be executed.
        
        Somebody handling the request could, e.g., use the connection for determining the identifier quote string, etc.
        """


__all__ = ['ParametersRequest']

