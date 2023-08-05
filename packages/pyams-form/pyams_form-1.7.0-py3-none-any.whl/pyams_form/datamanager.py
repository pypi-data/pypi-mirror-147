#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_form.datamanager module

This module provides base data manager classes.
"""

from zope.interface import implementer, Interface
from zope.interface.common.mapping import IMapping
from zope.schema.interfaces import IField
from zope.security import canAccess, canWrite
from zope.security.interfaces import ForbiddenAttribute
from zope.security.proxy import Proxy

from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import IDataManager, NO_VALUE


__docformat__ = 'restructuredtext'


_MARKER = []


ALLOWED_DATA_CLASSES = [dict]
try:
    import persistent.mapping
    import persistent.dict
    ALLOWED_DATA_CLASSES.append(persistent.mapping.PersistentMapping)
    ALLOWED_DATA_CLASSES.append(persistent.dict.PersistentDict)
except ImportError:
    pass


@implementer(IDataManager)
class DataManager:
    """Data manager base class."""


@adapter_config(required=(Interface, IField), provides=IDataManager)
class AttributeField(DataManager):
    """Attribute field."""

    def __init__(self, context, field):
        self.context = context
        self.field = field

    @property
    def adapted_context(self):
        """Data manager adapted context getter"""
        # get the right adapter or context
        context = self.context
        # NOTE: zope.schema fields defined in inherited interfaces will point
        # to the inherited interface. This could end in adapting the wrong item.
        # This is very bad because the widget field offers an explicit interface
        # argument which doesn't get used in Widget setup during IDataManager
        # lookup. We should find a concept which allows to adapt the
        # IDataManager use the widget field interface instead of the zope.schema
        # field.interface, ri
        if self.field.interface is not None:
            context = self.field.interface(context)
        return context

    def get(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        return getattr(self.adapted_context, self.field.__name__)

    def query(self, default=NO_VALUE):
        """See pyams_utils.interfaces.form.IDataManager"""
        try:
            return self.get()
        except ForbiddenAttribute as e:  # pylint: disable=invalid-name
            raise e
        except AttributeError:
            return default

    def set(self, value):
        """See pyams_utils.interfaces.form.IDataManager"""
        if self.field.readonly:
            raise TypeError("Can't set values on read-only fields (name=%s, class=%s.%s)" %
                            (self.field.__name__,
                             self.context.__class__.__module__,
                             self.context.__class__.__name__))
        # get the right adapter or context
        setattr(self.adapted_context, self.field.__name__, value)

    def can_access(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        context = self.adapted_context
        if isinstance(context, Proxy):
            return canAccess(context, self.field.__name__)
        return True

    def can_write(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        context = self.adapted_context
        if isinstance(context, Proxy):
            return canWrite(context, self.field.__name__)
        return True


@adapter_config(required=(dict, IField), provides=IDataManager)
class DictionaryField(DataManager):
    """Dictionary field.

    NOTE: Even though, this data manager allows nearly all kinds of
    mappings, by default it is only registered for dict, because it
    would otherwise get picked up in undesired scenarios. If you want
    to it use for another mapping, register the appropriate adapter in
    your application.

    """

    _allowed_data_classes = tuple(ALLOWED_DATA_CLASSES)

    def __init__(self, data, field):
        if (not isinstance(data, self._allowed_data_classes) and
                not IMapping.providedBy(data)):
            raise ValueError("Data are not a dictionary: %s" % type(data))
        self.data = data
        self.field = field

    def get(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        value = self.data.get(self.field.__name__, _MARKER)
        if value is _MARKER:
            raise AttributeError
        return value

    def query(self, default=NO_VALUE):
        """See pyams_utils.interfaces.form.IDataManager"""
        return self.data.get(self.field.__name__, default)

    def set(self, value):
        """See pyams_utils.interfaces.form.IDataManager"""
        if self.field.readonly:
            raise TypeError("Can't set values on read-only fields name=%s"
                            % self.field.__name__)
        self.data[self.field.__name__] = value

    @staticmethod
    def can_access():
        """See pyams_utils.interfaces.form.IDataManager"""
        return True

    @staticmethod
    def can_write():
        """See pyams_utils.interfaces.form.IDataManager"""
        return True
