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
# Namespace: com.sun.star.form.runtime
from typing_extensions import Literal
import typing
from ...lang.x_component import XComponent as XComponent_98dc0ab5
if typing.TYPE_CHECKING:
    from ...beans.named_value import NamedValue as NamedValue_a37a0af3
    from .feature_state import FeatureState as FeatureState_1c3f0ebb
    from .x_feature_invalidation import XFeatureInvalidation as XFeatureInvalidation_9f4211f4
    from .x_form_controller import XFormController as XFormController_4a570ffe
    from ...sdbc.x_result_set_update import XResultSetUpdate as XResultSetUpdate_e0fb0d0a
    from ...sdbc.x_row_set import XRowSet as XRowSet_7a090960

class XFormOperations(XComponent_98dc0ab5):
    """
    encapsulates operations on a database form.
    
    This instance allows for operations on a user interface form, by saving its clients from various tedious and error-prone operations.
    
    As an example, imagine you have a database form, displayed in some user interface, which you want to move to the next record.
    It is as easy as calling com.sun.star.sdbc.XResultSet.next() on this form, right? Wrong. First, you need to care for saving the current record, so the user doesn't lose her input. So you need to call com.sun.star.sdbc.XResultSetUpdate.updateRow() or com.sun.star.sdbc.XResultSetUpdate.insertRow(), depending on the form's com.sun.star.sdb.RowSet.IsNew property.
    But then you're done, right? Wrong, again.
    When the user just entered some data into one of the form fields, but did not yet leave this field, then the data is not yet committed to the form, not to talk about being committed to the underlying database. So, before everything else, you would need to obtain the active control of the form, and commit it.
    Now you're done ...
    
    As another example, consider that you want to delete the current record from the form. You have to take into account any com.sun.star.form.XConfirmDeleteListeners registered at the com.sun.star.form.FormController or the com.sun.star.form.component.DataForm.
    
    If you agree that this is ugly to do and maintain, then XFormOperations is for you. It provides an execute() method, which will do all of the above for you; plus some similar convenient wrappers for similar functionality.
    
    **since**
    
        OOo 2.2

    See Also:
        `API XFormOperations <https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1form_1_1runtime_1_1XFormOperations.html>`_
    """
    __pyunointerface__: Literal['com.sun.star.form.runtime.XFormOperations']

    def commitCurrentControl(self) -> bool:
        """
        commits the current control of our controller

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """
    def commitCurrentRecord(self, RecordInserted: bool) -> bool:
        """
        commits the current record of the form

        * ``RecordInserted`` is an out direction argument.

        Raises:
            com.sun.star.sdbc.SQLException: ``SQLException``
        """
    def execute(self, Feature: int) -> None:
        """
        executes the operation associated with the given feature

        Raises:
            : ````
            : ````
            com.sun.star.lang.WrappedTargetException: ``WrappedTargetException``
        """
    def executeWithArguments(self, Feature: int, Arguments: 'typing.Tuple[NamedValue_a37a0af3, ...]') -> None:
        """
        executes the operation associated with the given feature, with passing arguments for execution

        Raises:
            : ````
            : ````
            com.sun.star.lang.WrappedTargetException: ``WrappedTargetException``
        """
    def getState(self, Feature: int) -> 'FeatureState_1c3f0ebb':
        """
        retrieves the current state of the given feature
        
        You would usually use this to update some user interface to reflect this state. For instance, you could imagine a toolbar button which is associated with a given feature. This button would be enabled if and only if the respective feature is currently available, and be checked if and only if the feature state is a boolean evaluating to TRUE.
        """
    def isEnabled(self, Feature: int) -> bool:
        """
        determines whether a feature is currently enabled.
        
        Calling this is equivalent to calling getState(), and evaluating the FeatureState.Enabled member.
        """
    def isInsertionRow(self) -> bool:
        """
        determines whether the form is currently positioned on the insertion row
        
        This is a convenience method only. Calling it is equivalent to examining the com.sun.star.sdb.RowSet.IsNew property of the form.

        Raises:
            com.sun.star.lang.WrappedTargetException: ``WrappedTargetException``
        """
    def isModifiedRow(self) -> bool:
        """
        determines whether the current row of the form is modified
        
        This is a convenience method only. Calling it is equivalent to examining the com.sun.star.sdb.RowSet.IsModified property of the form.

        Raises:
            com.sun.star.lang.WrappedTargetException: ``WrappedTargetException``
        """
    @property
    def Controller(self) -> 'XFormController_4a570ffe':
        """
        provides access to the form controller which the instance is operating on.
        
        Note that it is possible to operate on a user interface form without actually having access to the form controller instance. However, in this case some functionality will not be available. In particular, every feature which relies on the active control of the controller might be of limited use.
        """

    @property
    def Cursor(self) -> 'XRowSet_7a090960':
        """
        provides access to the cursor of the form the instance is operating on.
        """

    @property
    def FeatureInvalidation(self) -> 'XFeatureInvalidation_9f4211f4':
        """
        denotes the instance which should be notified about features whose state might have changed.
        
        If this attribute is not NULL, the instance which it denotes will be notified whenever the state of any supported feature might have changed.
        
        For instance, imagine a form whose current row has just been moved to another record, using the execute() method. This means that potentially, the state of all movement-related features might have changed.
        
        Note that the instance does not actually notify changes in the feature states, but only potential changes: It's up to the callee to react on this appropriately. This is since OpenOffice.org's application framework features own mechanisms to cache and invalidate feature states, so we do not burden this implementation here with such mechanisms.
        """

    @property
    def UpdateCursor(self) -> 'XResultSetUpdate_e0fb0d0a':
        """
        provides access to the update cursor of the form the instance is operating on.
        """


