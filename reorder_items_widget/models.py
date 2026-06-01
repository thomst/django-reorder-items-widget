from django.db import models
from .widgets import ReorderItemsWidget


__all__ = (
    'ReorderItemsFieldMixin',
    'ReorderItemsField',
)


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

        super().__init__(*args, **kwargs)


class ReorderItemsField(ReorderItemsFieldMixin, models.PositiveSmallIntegerField):
    """
    A PositivSmallIntegerField using the :class:`.ReorderItemsFieldMixin`.
    """