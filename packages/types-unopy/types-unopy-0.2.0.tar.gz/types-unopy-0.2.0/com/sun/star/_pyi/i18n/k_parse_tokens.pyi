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
# Namespace: com.sun.star.i18n
from typing_extensions import Literal


class KParseTokens:
    """
    Const Class

    These constants specify the characters a name or identifier token to be parsed can have.
    
    They are passed to XCharacterClassification.parseAnyToken() and XCharacterClassification.parsePredefinedToken(). They are also set in the ParseResult.StartFlags and ParseResult.ContFlags.
    
    **since**
    
        LibreOffice 6.2

    See Also:
        `API KParseTokens <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1i18n_1_1KParseTokens.html>`_
    """
    ASC_UPALPHA: Literal[1]
    """
    ASCII A-Z upper alpha.
    """
    ASC_LOALPHA: Literal[2]
    """
    ASCII a-z lower alpha.
    """
    ASC_DIGIT: Literal[4]
    """
    ASCII 0-9 digit.
    """
    ASC_UNDERSCORE: Literal[8]
    """
    ASCII '_' underscore.
    """
    ASC_DOLLAR: Literal[16]
    """
    ASCII '$' dollar.
    """
    ASC_DOT: Literal[32]
    """
    ASCII '.' dot/point.
    """
    ASC_COLON: Literal[64]
    """
    ASCII ':' colon.
    """
    ASC_CONTROL: Literal[512]
    """
    Special value to allow control characters (0x00 < char < 0x20)
    """
    ASC_ANY_BUT_CONTROL: Literal[1024]
    """
    Special value to allow anything below 128 except control characters.
    
    Not set in ParseResult.
    """
    ASC_OTHER: Literal[2048]
    """
    Additional flag set in ParseResult.StartFlags or ParseResult.ContFlags.
    
    Set if none of the above ASC_... (except ASC_ANY_...) single values match an ASCII character parsed.
    """
    UNI_UPALPHA: Literal[4096]
    """
    Unicode (above 127) upper case letter.
    """
    UNI_LOALPHA: Literal[8192]
    """
    Unicode (above 127) lower case letter.
    """
    UNI_DIGIT: Literal[16384]
    """
    Unicode (above 127) decimal digit number.
    """
    UNI_TITLE_ALPHA: Literal[32768]
    """
    Unicode (above 127) title case letter.
    """
    UNI_MODIFIER_LETTER: Literal[65536]
    """
    Unicode (above 127) modifier letter.
    """
    UNI_OTHER_LETTER: Literal[131072]
    """
    Unicode (above 127) other letter.
    """
    UNI_LETTER_NUMBER: Literal[262144]
    """
    Unicode (above 127) letter number.
    """
    UNI_OTHER_NUMBER: Literal[524288]
    """
    Unicode (above 127) other number.
    """
    GROUP_SEPARATOR_IN_NUMBER: Literal[134217728]
    """
    If this bit is set in nContCharFlags parameters, the locale's group separator characters in numbers are accepted and ignored/skipped.
    
    Else a group separator in a number ends the current token. A leading group separator is never accepted. If an accepted group separator was encountered in a number (ParseResult.TokenType is KParseType.ASC_NUMBER or KParseType.UNI_NUMBER) this bit is also set in ParseResult.ContFlags.
    
    NOTE: absence of this bit in nContCharFlags changes the default behaviour that in prior releases accepted numbers with group separators but lead to unexpected results when parsing formula expressions where the user entered a (wrong) separator that happened to be the group separator instead of an intended decimal separator. Usually inline numbers in a formula expression do not contain group separators.
    
    **since**
    
        LibreOffice 6.2
    """
    TWO_DOUBLE_QUOTES_BREAK_STRING: Literal[268435456]
    """
    If this bit is set in nContCharFlags parameters and a string enclosed in double quotes is parsed and two consecutive double quotes are encountered, the string is ended.
    
    If this bit is not set, the two double quotes are parsed as one escaped double quote and string parsing continues. The bit is ignored in nStartCharFlags parameters.
    
    Example:
    \"abc\"\"def\" --> bit not set => abc\"def <br/>
    \"abc\"\"def\" --> bit set => abc
    """
    UNI_OTHER: Literal[536870912]
    """
    Additional flag set in ParseResult.StartFlags or ParseResult.ContFlags.
    
    Set if none of the above UNI_... single values match a Unicode character parsed.
    """
    IGNORE_LEADING_WS: Literal[1073741824]
    """
    Only valid for nStartCharFlags parameter to CharacterClassification.parseAnyToken() and CharacterClassification.parsePredefinedToken(), ignored on nContCharFlags parameter.
    
    Not set in ParseResult.
    """
    ASC_ALPHA: str
    """
    ASCII a-zA-Z lower or upper alpha.
    """
    ASC_ALNUM: str
    """
    ASCII a-zA-Z0-9 alphanumeric.
    """
    UNI_ALPHA: str
    """
    Unicode (above 127) lower or upper or title case alpha.
    """
    UNI_ALNUM: str
    """
    Unicode (above 127) alphanumeric.
    """
    UNI_LETTER: str
    """
    Unicode (above 127) alpha or letter.
    """
    UNI_NUMBER: str
    """
    Unicode (above 127) number.
    """
    ANY_ALPHA: str
    """
    any (ASCII or Unicode) alpha
    """
    ANY_DIGIT: str
    """
    any (ASCII or Unicode) digit
    """
    ANY_ALNUM: str
    """
    any (ASCII or Unicode) alphanumeric
    """
    ANY_LETTER: str
    """
    any (ASCII or Unicode) letter
    """
    ANY_NUMBER: str
    """
    any (ASCII or Unicode) number
    """
    ANY_LETTER_OR_NUMBER: str
    """
    any (ASCII or Unicode) letter or number
    """

