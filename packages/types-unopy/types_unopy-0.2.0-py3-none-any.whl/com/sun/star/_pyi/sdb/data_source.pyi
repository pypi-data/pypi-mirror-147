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
import typing
from ..beans.x_property_set import XPropertySet as XPropertySet_bc180bfa
from .x_bookmarks_supplier import XBookmarksSupplier as XBookmarksSupplier_ee870d96
from .x_completed_connection import XCompletedConnection as XCompletedConnection_98a0e46
from .x_query_definitions_supplier import XQueryDefinitionsSupplier as XQueryDefinitionsSupplier_5913107f
from ..sdbc.x_data_source import XDataSource as XDataSource_a2990ae7
from ..sdbc.x_isolated_connection import XIsolatedConnection as XIsolatedConnection_99c0e41
from ..util.x_flushable import XFlushable as XFlushable_9a420ab4
if typing.TYPE_CHECKING:
    from ..beans.property_value import PropertyValue as PropertyValue_c9610c73
    from ..util.x_number_formats_supplier import XNumberFormatsSupplier as XNumberFormatsSupplier_3afb0fb7

class DataSource(XPropertySet_bc180bfa, XBookmarksSupplier_ee870d96, XCompletedConnection_98a0e46, XQueryDefinitionsSupplier_5913107f, XDataSource_a2990ae7, XIsolatedConnection_99c0e41, XFlushable_9a420ab4):
    """
    Service Class

    is a factory to establish database connections.
    
    It should be registered at a com.sun.star.uno.NamingService.
    
    **since**
    
        OOo 1.1.2

    See Also:
        `API DataSource <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1sdb_1_1DataSource.html>`_
    """
    @property
    def Info(self) -> 'typing.Tuple[PropertyValue_c9610c73, ...]':
        """
        is a list of arbitrary string tag/value pairs as connection arguments
        
        The DataSource itself does not attempt to interpret any of those values.
        
        Instead, the values in this property have two use cases:
        """
    @property
    def TableFilter(self) -> 'typing.Tuple[str, ...]':
        """
        defines a list of tables, on which the DataSource should have it's focus.
        
        If empty, all tables are rejected.
        """
    @property
    def TableTypeFilter(self) -> 'typing.Tuple[str, ...]':
        """
        defines a list of table types, on which the DataSource should have it's focus.
        
        If empty, all table types are rejected.
        """
    @property
    def IsPasswordRequired(self) -> bool:
        """
        indicates that a password is always necessary.
        """
    @property
    def IsReadOnly(self) -> bool:
        """
        determines whether modifications on the data source are allowed or not.
        """
    @property
    def Name(self) -> str:
        """
        is the name of the data source.
        
        If the data source is registered at the database context, then the Name property denotes the registration name. Otherwise, the name property contains the URL of the file which the database document associated with the data source is based on.
        
        If the same data source is registered under different names, the value of the Name property is not defined.
        """
    @property
    def NumberFormatsSupplier(self) -> 'XNumberFormatsSupplier_3afb0fb7':
        """
        provides an object for formatting numbers.
        """
    @property
    def Password(self) -> str:
        """
        determines a users password.
        
        The password is not persistent.
        """
    @property
    def Settings(self) -> 'XPropertySet_bc180bfa':
        """
        is a convenience wrapper around the Info property.
        
        Since fiddling around with a sequence of property values is somewhat uncomfortable in all known UNO language bindings (especially for tasks like simply changing the value of an existing value), the Settings property wraps the Info property for easier single-value access.
        
        You should use the Settings property if you need to access a few properties only, and the Info property if you need access to all existent settings at once.
        
        The object represented by this property supports the com.sun.star.beans.PropertyBag service. That is, you can at runtime add arbitrary new properties to the bag.
        
        Additionally, the property bag supports default values of properties, and thus the com.sun.star.beans.XPropertyState interface. If you add an own property to the bag using com.sun.star.beans.XPropertyContainer.addProperty(), you need to specify an initial value, which is also used as default value (exceptions see below).
        
        Effectively, the property bag represented by Settings contains two classes of properties: Pre-defined ones and user-defined ones.
        
        Pre-defined properties are properties which are potentially used by the data source, the application UI for the data source, or a particular backend driver employed by the data source. There's a large set of such properties, no all of them are effectively used for a concrete data source, nonetheless, they're all present in the Settings.
        Such properties are not removable from the bag, that is, their com.sun.star.beans.PropertyAttribute.REMOVABLE attribute is not set.
        Usually, you'll find that all of this properties have the com.sun.star.beans.PropertyState.PropertyState_DEFAULT_VALUE state.
        
        User-defined properties are the ones which are added at runtime by any instance. They might or might not be removable, this depends on whether or not the code adding them specifies the com.sun.star.beans.PropertyAttribute.REMOVABLE attribute. Also, they might or might not have a default value, determined by the com.sun.star.beans.PropertyAttribute.MAYBEDEFAULT attribute at the time they're added to the bag.
        
        When a data source is made persistent, then properties which are not removable (which are assumed to be the pre-defined properties) are ignored when they are in DEFAULT state. All other properties are always made persistent, except when an explicit com.sun.star.beans.PropertyAttribute.TRANSIENT attribute prohibits this.
        
        Similar, when you obtain the Info property of a DataSource, the Settings bag is asked for all its property values, and the ones which are removable and in state default are stripped, and not returned in the Info sequence.
        """
    @property
    def SuppressVersionColumns(self) -> bool:
        """
        indicates that components displaying data obtained from this data source should suppress columns used for versioning.
        """
    @property
    def URL(self) -> str:
        """
        indicates a database url of the form
        jdbc:subprotocol:subname or sdbc:subprotocol:subname
        """
    @property
    def User(self) -> str:
        """
        determines a users login name.
        """


