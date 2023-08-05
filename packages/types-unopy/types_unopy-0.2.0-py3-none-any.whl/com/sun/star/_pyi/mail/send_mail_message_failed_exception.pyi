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
# Namespace: com.sun.star.mail
# Libre Office Version: 7.3
from typing_extensions import Literal
from ooo.oenv.env_const import UNO_NONE
import typing
from .mail_exception import MailException as MailException_ba9e0bdd
from ..uno.x_interface import XInterface as XInterface_8f010a43

class SendMailMessageFailedException(MailException_ba9e0bdd):
    """
    Exception Class

    A SendFailedException will be thrown if a mail message could not be sent because the e-mail addresses of some recipients are invalid.
    
    E-mail addresses have to conform to RFC 822.
    
    **since**
    
        OOo 2.0

    See Also:
        `API SendMailMessageFailedException <https://api.libreoffice.org/docs/idl/ref/exceptioncom_1_1sun_1_1star_1_1mail_1_1SendMailMessageFailedException.html>`_
    """

    typeName: Literal['com.sun.star.mail.SendMailMessageFailedException']

    def __init__(self, Message: typing.Optional[str] = ..., Context: typing.Optional[XInterface_8f010a43] = ..., InvalidAddresses: typing.Optional[typing.Tuple[str, ...]] = ..., ValidSentAddresses: typing.Optional[typing.Tuple[str, ...]] = ..., ValidUnsentAddresses: typing.Optional[typing.Tuple[str, ...]] = ...) -> None:
        """
        Constructor

        Arguments:
            Message (str, optional): Message value.
            Context (XInterface, optional): Context value.
            InvalidAddresses (typing.Tuple[str, ...], optional): InvalidAddresses value.
            ValidSentAddresses (typing.Tuple[str, ...], optional): ValidSentAddresses value.
            ValidUnsentAddresses (typing.Tuple[str, ...], optional): ValidUnsentAddresses value.
        """
    @property
    def InvalidAddresses(self) -> typing.Tuple[str, ...]:
        """
        The addresses which are invalid because they do not conform to RFC 822.
        """

    @property
    def ValidSentAddresses(self) -> typing.Tuple[str, ...]:
        """
        The addresses to which the mail message was sent successfully.
        """

    @property
    def ValidUnsentAddresses(self) -> typing.Tuple[str, ...]:
        """
        The addresses which are valid but to which the message was not sent.
        """


__all__ = ['SendMailMessageFailedException']

