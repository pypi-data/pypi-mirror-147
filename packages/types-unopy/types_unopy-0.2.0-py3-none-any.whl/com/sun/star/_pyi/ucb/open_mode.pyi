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
# Namespace: com.sun.star.ucb
from typing_extensions import Literal


class OpenMode:
    """
    Const Class

    These are the possible values for OpenCommandArgument.Mode.

    See Also:
        `API OpenMode <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1ucb_1_1OpenMode.html>`_
    """
    ALL: Literal[0]
    """
    open a folder, include all children in result set (documents and folders).
    """
    FOLDERS: Literal[1]
    """
    open a folder, include only children, that are folders, in result set.
    """
    DOCUMENTS: Literal[3]
    """
    open a folder, include only children, that are documents, in result set.
    """
    DOCUMENT: Literal[2]
    """
    open a document.
    
    There are no special requirements for data access sharing.
    
    Note: There must be a data sink supplied in the OpenCommandArgument struct, if this value is set. This sink will be used by the content implementation to supply the document data.
    """
    DOCUMENT_SHARE_DENY_NONE: Literal[4]
    """
    open a document.
    
    Allow shared read and write access.
    
    Note: There must be a data sink supplied in the OpenCommandArgument struct, if this value is set. This sink will be used by the content implementation to supply the document data.
    """
    DOCUMENT_SHARE_DENY_WRITE: Literal[5]
    """
    open a document.
    
    Deny shared write access.
    
    Note: There must be a data sink supplied in the OpenCommandArgument struct, if this value is set. This sink will be used by the content implementation to supply the document data.
    """

