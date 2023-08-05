#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_skin.interfaces module

This module provides general skin-related interfaces.
"""
from collections import OrderedDict

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


__docformat__ = 'restructuredtext'

from pyams_skin import _


BOOTSTRAP_STATUS = ('primary', 'secondary', 'success', 'danger',
                    'warning', 'info', 'light', 'dark')
"""Bootstrap status list"""


BOOTSTRAP_SIZES = OrderedDict((
    ('xs', _("Smartphones")),
    ('sm', _("Tablets")),
    ('md', _("Medium screens")),
    ('lg', _("Large screens")),
    ('xl', _("Extra large screens"))
))

BOOTSTRAP_SIZES_VOCABULARY = SimpleVocabulary([
    SimpleTerm(v, title=t)
    for v, t in BOOTSTRAP_SIZES.items()
])
