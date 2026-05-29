from django.db import models
from .widgets import ReorderItemsWidget


class ReorderItemsFieldMixin:
    """
    This mixin makes any kind of integer fields to an index field for reordering
    purposes.

    TODO
    """

    def __init__(self, *args, grouped_by=None, **kwargs):
        self.grouped_by = grouped_by

        # Check for unique parameter. It must not be True.
        if kwargs.get('unique'):
            msg = 'Do not use unique=True with a ReorderItemsField. '
            msg += 'This will cause trouble updating its values.'
            raise ValueError(msg)

        # We need blank=True since the form field will be hidden and updated
        # by a pre_save signal handler.
        kwargs['blank'] = True

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        Customising the ``form_class``.

        :return: IntegerField with a custom ``form_class``.
        :rtype: django.db.models.IntegerField
        """
        kwargs['widget'] = ReorderItemsWidget()
        return super().formfield(**kwargs)


class ReorderItemsField(ReorderItemsFieldMixin, models.PositiveSmallIntegerField):
    """
    A PositivSmallIntegerField using the :class:`.ReorderItemsFieldMixin`.
    """