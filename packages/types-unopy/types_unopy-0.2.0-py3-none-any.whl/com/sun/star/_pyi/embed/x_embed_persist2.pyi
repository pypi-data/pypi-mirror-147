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
# Namespace: com.sun.star.embed
from typing_extensions import Literal
from .x_embed_persist import XEmbedPersist as XEmbedPersist_c5660c24

class XEmbedPersist2(XEmbedPersist_c5660c24):
    """

    See Also:
        `API XEmbedPersist2 <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1embed_1_1XEmbedPersist2.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.embed.XEmbedPersist2']

    def isStored(self) -> bool:
        """
        Checks whether or not the object has created its persistent representation counterpart of its in-memory model.
        """

