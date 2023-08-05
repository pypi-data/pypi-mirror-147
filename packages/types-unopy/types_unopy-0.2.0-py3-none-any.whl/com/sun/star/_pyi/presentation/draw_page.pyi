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
# Service Class
# this is a auto generated file generated by Cheetah
# Libre Office Version: 7.3
# Namespace: com.sun.star.presentation
import typing
from ..document.link_target import LinkTarget as LinkTarget_ca220c5c
from ..drawing.draw_page import DrawPage as DrawPage_a56e0aff
if typing.TYPE_CHECKING:
    from .animation_speed import AnimationSpeed as AnimationSpeed_3fb20fb5
    from .fade_effect import FadeEffect as FadeEffect_1890de1

class DrawPage(LinkTarget_ca220c5c, DrawPage_a56e0aff):
    """
    Service Class

    This is the service provided by a com.sun.star.drawing.DrawPage inside a PresentationDocument.
    
    **since**
    
        LibreOffice 6.1

    See Also:
        `API DrawPage <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1presentation_1_1DrawPage.html>`_
    """
    @property
    def Change(self) -> int:
        """
        specifies how the page change is triggered.
        
        If this is 0, the user must click to start each object animation and to change the page. If set to 1, the page is automatically switched. If it is set to 2, all object effects run automatically, but the user has to click on the page to change it.
        """
    @property
    def DateTimeFormat(self) -> int:
        """
        defines the format that is used to format a date and time text field on this page.
        
        This is only used if IsDateTimeFixed is FALSE.
        """
    @property
    def DateTimeText(self) -> str:
        """
        defines the text that is displayed in a date and time textfield rendered on this page.
        
        This value is only used if IsDateTimeFixed is TRUE.
        """
    @property
    def Duration(self) -> int:
        """
        If the property com.sun.star.drawing.DrawPage.Change is set to 1, this is the time in seconds this page is shown before switching to the next page.
        """
    @property
    def Effect(self) -> 'FadeEffect_1890de1':
        """
        This is the effect that is used to fade in this page.
        """
    @property
    def FooterText(self) -> str:
        """
        defines the text that is displayed in a footer textfield rendered on this page.
        """
    @property
    def HeaderText(self) -> str:
        """
        defines the text that is displayed in a header textfield rendered on this page.
        """
    @property
    def HighResDuration(self) -> float:
        """
        If the property com.sun.star.drawing.DrawPage.Change is set to 1, this is the time in seconds this page is shown before switching to the next page, also permitting sub-second precision here.
        """
    @property
    def IsDateTimeFixed(self) -> bool:
        """
        defines if a date and time text field shows a fixed string value or the current date on this page.
        """
    @property
    def IsDateTimeVisible(self) -> bool:
        """
        defines if a date and time presentation shape from the master page is visible on this page.
        """
    @property
    def IsFooterVisible(self) -> bool:
        """
        defines if a footer presentation shape from the master page is visible on this page.
        """
    @property
    def IsHeaderVisible(self) -> bool:
        """
        defines if a header presentation shape from the master page is visible on this page.
        """
    @property
    def IsPageNumberVisible(self) -> bool:
        """
        defines if a page number presentation shape from the master page is visible on this page.
        """
    @property
    def Layout(self) -> int:
        """
        If this property is not ZERO, this number specifies a presentation layout for this page.
        """
    @property
    def Speed(self) -> 'AnimationSpeed_3fb20fb5':
        """
        Defines the speed of the fade-in effect of this page.
        """
    @property
    def TransitionDuration(self) -> float:
        """
        Specifies slide transition time in seconds.
        
        **since**
        
            LibreOffice 6.1
        """


