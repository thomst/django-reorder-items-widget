from django.db import models


class ReorderItemsField(models.PositiveSmallIntegerField):
    """
    A field to store the index of an item for reordering purposes.

    This is a PositiveSmallIntegerField with some customizations:
    You can
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
