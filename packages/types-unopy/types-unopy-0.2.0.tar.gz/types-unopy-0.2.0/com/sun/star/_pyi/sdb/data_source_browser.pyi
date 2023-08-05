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
# Namespace: com.sun.star.sdb
from ..form.form_controller import FormController as FormController_c9180c74
from ..frame.x_controller import XController as XController_b00e0b8f
from ..frame.x_dispatch_provider import XDispatchProvider as XDispatchProvider_fc690de6
from ..lang.x_initialization import XInitialization as XInitialization_d46c0cca
from ..ui.x_context_menu_interception import XContextMenuInterception as XContextMenuInterception_38f90fac

class DataSourceBrowser(FormController_c9180c74, XController_b00e0b8f, XDispatchProvider_fc690de6, XInitialization_d46c0cca, XContextMenuInterception_38f90fac):
    """
    Service Class

    implements a component which allows browsing the data sources registered on the system.
    
    This service implements a user interface for browsing data sources registered on the com.sun.star.sdb.DatabaseContext instance of the system.
    
    It is possible to navigate through all the data sources, it's queries and it's tables. The queries/tables can be displayed in a grid-like view, where functionality for searching, sorting, filtering, and such is provided.
    
    Usually, you won't instantiate this service directly, instead you use the dispatch mechanisms of the application framework to load the URL .component:DB/DataSourceBrowser into an arbitrary frame. This should involve a com.sun.star.sdb.ContentLoader service, which creates and initializes the browser.
    
    Some aspects of the browser can be controlled from outside, e.g., it is possible to dispatch a sort or filter request, if a table or query is being displayed.
    
    The communication between the browser and external instances works in two ways.
    The way in is provided by the com.sun.star.frame.XDispatchProvider interface the service exports (Please see below for more details on this).
    The way out works in another way. There are several URLs which an external instance can provide dispatches for (usually by implementing a com.sun.star.frame.XDispatchProviderInterceptor for the parent frame of the browser), thus indicating that the browser should provide special functionality.
    In this case, the browser displays and maintains some additional slots (to be more concrete: toolbox items), which, upon triggering, call the com.sun.star.frame.XDispatch.dispatch() method of the object provided by the external instance.
    
    In particular, the supported URLs for communicating to an external instance are:
    
    For all kinds of URLs, the parameters supplied during dispatching build up a DataAccessDescriptor, where the following properties are present:
    
    The default for DataAccessDescriptor.Selection is to contain bookmarks, if not specified otherwise by DataAccessDescriptor.BookmarkSelection.
    
    **since**
    
        OOo 3.0

    See Also:
        `API DataSourceBrowser <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sdb_1_1DataSourceBrowser.html>`_
    """


