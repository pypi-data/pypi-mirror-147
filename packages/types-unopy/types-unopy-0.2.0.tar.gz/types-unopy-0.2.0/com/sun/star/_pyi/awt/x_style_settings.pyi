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
# Namespace: com.sun.star.awt
from typing_extensions import Literal
import typing
from abc import ABC
if typing.TYPE_CHECKING:
    from .font_descriptor import FontDescriptor as FontDescriptor_bc110c0a
    from .x_style_change_listener import XStyleChangeListener as XStyleChangeListener_ad50e49
    from ..util.color import Color as Color_68e908c5

class XStyleSettings(ABC):
    """
    provides access to certain style settings within an OpenOffice.org component, such as a window, or within OpenOffice.org as a whole.
    
    Note that there are constraints for those settings. For instance, if controls are drawn with the native widget framework, i.e. in the desktop theme's look, then they won't necessarily respect all their style settings, because those have a lesser priority than the native look.
    
    On the other hand, some settings are respected only when rendering the controls in the native desktop/theme look. For instance, without native theming, buttons do not support a \"roll over\" mode, i.e., they're painted the same way, no matter if they mouse hovers over them or not. But with native theming, this changes, as here the general button look is drawn by the system's theming engine, while the text is drawn by OpenOffice.org. In this case, the button respects the ButtonRolloverTextColor when painting its text.

    See Also:
        `API XStyleSettings <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XStyleSettings.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.awt.XStyleSettings']

    def addStyleChangeListener(self, Listener: 'XStyleChangeListener_ad50e49') -> None:
        """
        registers a listener to be notified when the style settings change
        """
    def removeStyleChangeListener(self, Listener: 'XStyleChangeListener_ad50e49') -> None:
        """
        registers a listener to be notified when the style settings change
        """
    @property
    def ActiveBorderColor(self) -> 'Color_68e908c5':
        """
        specifies the color of the border of active windows
        """

    @property
    def ActiveColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def ActiveTabColor(self) -> 'Color_68e908c5':
        """
        specifies the color of the active tab of a tab control
        """

    @property
    def ActiveTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for active UI components
        """

    @property
    def ApplicationFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the application font
        """

    @property
    def ButtonRolloverTextColor(self) -> 'Color_68e908c5':
        """
        specifies the color to use for text on buttons which are hovered with the mouse
        """

    @property
    def ButtonTextColor(self) -> 'Color_68e908c5':
        """
        specifies the color to use for text on buttons
        """

    @property
    def CheckedColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def DarkShadowColor(self) -> 'Color_68e908c5':
        """
        specifies the dark portion of the shadow to use for UI elements
        """

    @property
    def DeactiveBorderColor(self) -> 'Color_68e908c5':
        """
        specifies the color of the border of inactive windows
        """

    @property
    def DeactiveColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def DeactiveTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for inactive UI components
        """

    @property
    def DialogColor(self) -> 'Color_68e908c5':
        """
        specifies the background color of dialogs
        """

    @property
    def DialogTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color of dialogs
        """

    @property
    def DisableColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for disabled UI elements
        """

    @property
    def FaceColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def FaceGradientColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def FieldColor(self) -> 'Color_68e908c5':
        """
        specifies the background color for dialog input controls
        """

    @property
    def FieldFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font for dialog input controls
        """

    @property
    def FieldRolloverTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for dialog input controls which are hovered with the mouse
        """

    @property
    def FieldTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for dialog input controls
        """

    @property
    def FloatTitleFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font to use the title of floating windows
        """

    @property
    def GroupFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font for dialog elements used for grouping other elements
        """

    @property
    def GroupTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for dialog elements used for grouping other elements
        """

    @property
    def HelpColor(self) -> 'Color_68e908c5':
        """
        specifies the background color for dialog elements displaying help content
        """

    @property
    def HelpFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the help font
        """

    @property
    def HelpTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for dialog elements displaying help content
        """

    @property
    def HighContrastMode(self) -> bool:
        """
        controls whether the an UI component should use a high-contrast mode
        """

    @property
    def HighlightColor(self) -> 'Color_68e908c5':
        """
        specifies the background color for UI elements which are highlighted
        """

    @property
    def HighlightTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color for UI elements which are highlighted
        """

    @property
    def InactiveTabColor(self) -> 'Color_68e908c5':
        """
        specifies the color of inactive tabs of a tab control
        """

    @property
    def LabelFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font for label controls
        """

    @property
    def LabelTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color of label elements in dialogs
        """

    @property
    def LightColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def MenuBarColor(self) -> 'Color_68e908c5':
        """
        specifies the background color of menu bars
        """

    @property
    def MenuBarTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color of menu bars
        """

    @property
    def MenuBorderColor(self) -> 'Color_68e908c5':
        """
        specifies the border color of menus
        """

    @property
    def MenuColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def MenuFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font to use for menus
        """

    @property
    def MenuHighlightColor(self) -> 'Color_68e908c5':
        """
        specifies the background color of highlighted menu items
        """

    @property
    def MenuHighlightTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color of highlighted menu items
        """

    @property
    def MenuTextColor(self) -> 'Color_68e908c5':
        """
        """

    @property
    def MonoColor(self) -> 'Color_68e908c5':
        """
        specifies the color to use for monochrome control elements such as flat borders of controls
        """

    @property
    def PushButtonFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font of push buttons
        """

    @property
    def RadioCheckFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font of radio buttons and check boxes
        """

    @property
    def RadioCheckTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color of radio buttons and check boxes
        """

    @property
    def SeparatorColor(self) -> 'Color_68e908c5':
        """
        specifies the color of separators between UI elements
        """

    @property
    def ShadowColor(self) -> 'Color_68e908c5':
        """
        specifies the color to use for UI elements
        """

    @property
    def TitleFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font to use for window titles
        """

    @property
    def ToolFont(self) -> 'FontDescriptor_bc110c0a':
        """
        specifies the font to use for tool elements
        """

    @property
    def WindowColor(self) -> 'Color_68e908c5':
        """
        specifies the background color to use for non-dialog windows
        """

    @property
    def WindowTextColor(self) -> 'Color_68e908c5':
        """
        specifies the text color to use for non-dialog windows
        """

    @property
    def WorkspaceColor(self) -> 'Color_68e908c5':
        """
        specifies the background color to use for document workspaces
        """


