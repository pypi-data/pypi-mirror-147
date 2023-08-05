#
# Copyright (c) 2015-2022 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from zope.interface import implementer_only
from zope.schema.vocabulary import getVocabularyRegistry

from pyams_file.interfaces.thumbnail import THUMBNAILERS_VOCABULARY_NAME
from pyams_form.browser.widget import HTMLFormElement
from pyams_form.converter import BaseDataConverter
from pyams_form.interfaces import IDataConverter
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.widget import FieldWidget, Widget
from pyams_layer.interfaces import IFormLayer
from pyams_skin.interfaces import BOOTSTRAP_SIZES, BOOTSTRAP_SIZES_VOCABULARY
from pyams_skin.interfaces.schema import BootstrapThumbnailSelection, \
    IBootstrapThumbnailsSelectionDictField
from pyams_skin.interfaces.widget import IBootstrapThumbnailsSelectionDictWidget
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import NO_VALUE


@adapter_config(required=(IBootstrapThumbnailsSelectionDictField,
                          IBootstrapThumbnailsSelectionDictWidget),
                provides=IDataConverter)
class BootstrapThumbnailsSelectionDictDataConverter(BaseDataConverter):
    """Bootstrap thumbnails selection data converter"""

    def to_widget_value(self, value):
        return value

    def to_field_value(self, value):
        return value


@implementer_only(IBootstrapThumbnailsSelectionDictWidget)
class BootstrapThumbnailsSelectionDictWidget(HTMLFormElement, Widget):
    """Bootstrap selection widget"""

    @property
    def display_value(self):
        """Display value getter"""
        value = self.value
        if not value:
            value = {}
            for size in BOOTSTRAP_SIZES.keys():
                value[size] = BootstrapThumbnailSelection(cols=self.field.default_width)
        return value

    def extract(self, default=NO_VALUE):
        """Widget value extractor"""
        params = self.request.params
        marker = params.get(f'{self.name}-empty-marker', default)
        if marker is not default:
            result = {}
            for size in BOOTSTRAP_SIZES.keys():
                result[size] = BootstrapThumbnailSelection(
                    selection=params.get(f'{self.name}-{size}-selection'),
                    cols=params.get(f'{self.name}-{size}-cols', self.field.default_width))
            return result
        return default

    @property
    def bootstrap_sizes(self):
        """Bootstrap sizes getter"""
        return BOOTSTRAP_SIZES_VOCABULARY

    @property
    def thumbnails_selections(self):
        """Thumbnails selections getter"""
        return getVocabularyRegistry().get(self.context, THUMBNAILERS_VOCABULARY_NAME)


@adapter_config(required=(IBootstrapThumbnailsSelectionDictField, IFormLayer),
                provides=IFieldWidget)
def BootstrapThumbnailsSelectionDictFieldWidget(field, request):
    """Bootstrap thumbnails selection field widget factory"""
    return FieldWidget(field, BootstrapThumbnailsSelectionDictWidget(request))
