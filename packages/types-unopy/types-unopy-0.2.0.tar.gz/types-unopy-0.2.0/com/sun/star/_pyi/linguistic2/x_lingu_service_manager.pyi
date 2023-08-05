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
# Namespace: com.sun.star.linguistic2
from typing_extensions import Literal
import typing
from ..uno.x_interface import XInterface as XInterface_8f010a43
if typing.TYPE_CHECKING:
    from ..lang.locale import Locale as Locale_70d308fa
    from ..lang.x_event_listener import XEventListener as XEventListener_c7230c4a
    from .x_hyphenator import XHyphenator as XHyphenator_ff4e0def
    from .x_spell_checker import XSpellChecker as XSpellChecker_1af30e82
    from .x_thesaurus import XThesaurus as XThesaurus_f1790d91

class XLinguServiceManager(XInterface_8f010a43):
    """
    the basic interface to be used to access linguistic functionality.
    
    This interface is used to access spell checker, hyphenator, and thesaurus functionality. Additionally, it can query what implementations of those services are available (for specific languages or in general). It can select and query which of those implementations should be used for a specific language.
    
    For spell checking and thesaurus, the order in the list defines the order of creation/usage of those services. That is, if the first spell checker implementation does not recognize the given word as correct, the second service implementation for that language is created and gets queried. If that one fails, the third one gets created and queried and so on. This chain stops if an implementation reports the word as correct or the end of the list is reached, in which case the word is reported as incorrect.
    
    For the thesaurus, the behavior is the same when no meaning was found.

    See Also:
        `API XLinguServiceManager <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1linguistic2_1_1XLinguServiceManager.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.linguistic2.XLinguServiceManager']

    def addLinguServiceManagerListener(self, xListener: 'XEventListener_c7230c4a') -> bool:
        """
        adds a listener to the list of event listeners.
        
        The listeners may support one or both of com.sun.star.linguistic2.XDictionaryEventListener and com.sun.star.linguistic2.XLinguServiceEventListener interfaces.
        """
    def getAvailableServices(self, aServiceName: str, aLocale: 'Locale_70d308fa') -> 'typing.Tuple[str, ...]':
        """
        """
    def getConfiguredServices(self, aServiceName: str, aLocale: 'Locale_70d308fa') -> 'typing.Tuple[str, ...]':
        """
        queries the list of service implementations to be used for a given service and language.
        """
    def getHyphenator(self) -> 'XHyphenator_ff4e0def':
        """
        """
    def getSpellChecker(self) -> 'XSpellChecker_1af30e82':
        """
        """
    def getThesaurus(self) -> 'XThesaurus_f1790d91':
        """
        """
    def removeLinguServiceManagerListener(self, xListener: 'XEventListener_c7230c4a') -> bool:
        """
        removes a listener from the list of event listeners.
        """
    def setConfiguredServices(self, aServiceName: str, aLocale: 'Locale_70d308fa', aServiceImplNames: 'typing.Tuple[str, ...]') -> None:
        """
        sets the list of service implementations to be used for a given service and language.
        """

