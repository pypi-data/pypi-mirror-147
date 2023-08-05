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
# Const Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.datatransfer.dnd
from typing_extensions import Literal


class DNDConstants:
    """
    Const Class

    These values represent the type of action or actions to be performed by a Drag and Drop operation.

    See Also:
        `API DNDConstants <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1datatransfer_1_1dnd_1_1DNDConstants.html>`_
    """
    ACTION_NONE: Literal[0]
    """
    No action.
    """
    ACTION_COPY: Literal[1]
    """
    Action copy.
    """
    ACTION_MOVE: Literal[2]
    """
    Action move.
    """
    ACTION_COPY_OR_MOVE: Literal[3]
    """
    Action copy or move.
    """
    ACTION_LINK: Literal[4]
    """
    Action link.
    """
    ACTION_REFERENCE: Literal[4]
    """
    Action reference.
    """
    ACTION_DEFAULT: Literal[-128]
    """
    Action default.
    """

