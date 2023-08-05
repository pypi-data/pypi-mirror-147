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
# Struct Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.xml.crypto.sax
# Libre Office Version: 7.3
from typing_extensions import Literal
import typing
from ...sax.x_attribute_list import XAttributeList as XAttributeList_eec70d7b


class ElementStackItem(object):
    """
    Struct Class

    A struct to keep a startElement/endElement SAX event.

    See Also:
        `API ElementStackItem <https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1xml_1_1crypto_1_1sax_1_1ElementStackItem.html>`_
    """
    typeName: Literal['com.sun.star.xml.crypto.sax.ElementStackItem']

    def __init__(self, isStartElementEvent: typing.Optional[bool] = ..., elementName: typing.Optional[str] = ..., xAttributes: typing.Optional[XAttributeList_eec70d7b] = ...) -> None:
        """
        Constructor

        Arguments:
            isStartElementEvent (bool, optional): isStartElementEvent value.
            elementName (str, optional): elementName value.
            xAttributes (XAttributeList, optional): xAttributes value.
        """


    @property
    def isStartElementEvent(self) -> bool:
        """
        whether it is a startElement event
        """


    @property
    def elementName(self) -> str:
        """
        the name of the element
        """


    @property
    def xAttributes(self) -> XAttributeList_eec70d7b:
        """
        attribute list for a startElement event
        """


