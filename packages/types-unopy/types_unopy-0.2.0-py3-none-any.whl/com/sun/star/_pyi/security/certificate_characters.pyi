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
# Namespace: com.sun.star.security
from typing_extensions import Literal


class CertificateCharacters:
    """
    Const Class

    Constant definition of a certificate characters.
    
    The certificate characters will be defined as bit-wise constants.

    See Also:
        `API CertificateCharacters <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1security_1_1CertificateCharacters.html>`_
    """
    SELF_SIGNED: Literal[1]
    """
    It is a self-signed certificate.
    """
    HAS_PRIVATE_KEY: Literal[4]
    """
    A private key binding with the certificate is in user's profile.
    """

