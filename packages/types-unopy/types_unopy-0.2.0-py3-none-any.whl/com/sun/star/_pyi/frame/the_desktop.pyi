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
# Singleton Class
# this is a auto generated file generated by Cheetah
# Namespace: com.sun.star.frame
# Libre Office Version: 7.3
from .x_desktop2 import XDesktop2 as XDesktop2_98eb0a77


class theDesktop(XDesktop2_98eb0a77):
    """
    Singleton Class

    is the environment for components which can instantiate within frames
    
    A desktop environment contains tasks with one or more frames in which components can be loaded. The term \"task\" or naming a frame as a \"task frame\" is not in any way related to any additional implemented interfaces, it's just because these frames use task windows.
    
    Prior to LibreOffice 4.3, this singleton was only available as a (single-instance) Desktop service.
    
    **since**
    
        LibreOffice 4.3

    See Also:
        `API theDesktop <https://api.libreoffice.org/docs/idl/ref/singletoncom_1_1sun_1_1star_1_1frame_1_1theDesktop.html>`_
    """


