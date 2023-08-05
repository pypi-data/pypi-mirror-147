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
# Namespace: com.sun.star.script.provider
from typing_extensions import Literal


class ScriptFrameworkErrorType:
    """
    Const Class

    is a checked exception that represents an error encountered by the Scripting Framework whilst executing a script

    See Also:
        `API ScriptFrameworkErrorType <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1script_1_1provider_1_1ScriptFrameworkErrorType.html>`_
    """
    UNKNOWN: Literal[0]
    """
    Unknown.
    """
    NOTSUPPORTED: Literal[1]
    """
    ProviderNotSupported.
    """
    NO_SUCH_SCRIPT: Literal[2]
    """
    the requested method, and/or with the requested signature, does not exist
    """
    MALFORMED_URL: Literal[3]
    """
    the requested method, with the requested signature, does not exist
    """

