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
# Namespace: com.sun.star.drawing.framework
from typing_extensions import Literal
from .x_resource import XResource as XResource_3bcd0f90

class XView(XResource_3bcd0f90):
    """
    A view in the drawing framework is any object that paints into a pane.
    
    Typical examples are the Impress views that show a graphical representation of a document. But the task pane, which is primarily a container of dialogs, is a view as well.
    
    Luckily the drawing framework does not need to know much about what a view is. It just needs to identify view objects and a typesafe way to reference them.
    
    The URL prefix of views is private:resource/view

    See Also:
        `API XView <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1drawing_1_1framework_1_1XView.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.drawing.framework.XView']


