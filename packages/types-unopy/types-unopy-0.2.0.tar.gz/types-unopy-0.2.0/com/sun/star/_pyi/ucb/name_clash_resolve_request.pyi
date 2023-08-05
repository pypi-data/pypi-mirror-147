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
# Namespace: com.sun.star.ucb
# Libre Office Version: 7.3
from typing_extensions import Literal
from ooo.oenv.env_const import UNO_NONE
import typing
from ..task.classified_interaction_request import ClassifiedInteractionRequest as ClassifiedInteractionRequest_9f72121b
from ..uno.x_interface import XInterface as XInterface_8f010a43
from ..task.interaction_classification import InteractionClassification as InteractionClassification_6c4d10e7

class NameClashResolveRequest(ClassifiedInteractionRequest_9f72121b):
    """
    Exception Class

    This request is used to indicate a name clash.
    
    For example, when copying a file there might be another file in the target folder that has the same file name as the source file.
    
    If this exception is passed to an com.sun.star.task.XInteractionHandler an XInteractionSupplyName and an XInteractionReplaceExistingData should be supplied with the com.sun.star.task.XInteractionRequest. On return the XInteractionSupplyName, if selected, will contain a new name supposed to resolve the name clash. The XInteractionReplaceExistingData will be selected if the clashing resource shall be overwritten.

    See Also:
        `API NameClashResolveRequest <https://api.libreoffice.org/docs/idl/ref/exceptioncom_1_1sun_1_1star_1_1ucb_1_1NameClashResolveRequest.html>`_
    """

    typeName: Literal['com.sun.star.ucb.NameClashResolveRequest']

    def __init__(self, Message: typing.Optional[str] = ..., Context: typing.Optional[XInterface_8f010a43] = ..., Classification: typing.Optional[InteractionClassification_6c4d10e7] = ..., TargetFolderURL: typing.Optional[str] = ..., ClashingName: typing.Optional[str] = ..., ProposedNewName: typing.Optional[str] = ...) -> None:
        """
        Constructor

        Arguments:
            Message (str, optional): Message value.
            Context (XInterface, optional): Context value.
            Classification (InteractionClassification, optional): Classification value.
            TargetFolderURL (str, optional): TargetFolderURL value.
            ClashingName (str, optional): ClashingName value.
            ProposedNewName (str, optional): ProposedNewName value.
        """
    @property
    def TargetFolderURL(self) -> str:
        """
        contains the URL of the folder that contains the clashing resource.
        """

    @property
    def ClashingName(self) -> str:
        """
        contains the clashing name.
        """

    @property
    def ProposedNewName(self) -> str:
        """
        contains a proposal for a new, non-clashing name.
        
        This field may be left empty if the implementation is not able to suggest a new name.
        """


__all__ = ['NameClashResolveRequest']

