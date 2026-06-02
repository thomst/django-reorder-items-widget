from django.db import models


__all__ = (
    'UsingReorderItemsAdminMixin',
    'UsingReorderItemsSignalsMixin',
    'ReorderItemsField',
)

class UsingReorderItemsAdminMixin:
    """
    This mixin makes a integer field known by the reorder items admin classes.
    (See :mod:`~.admin` for more details.)

    Since :class:`~.admin.ReorderItemsModelAdminMixin` excludes the reorder
    items field from the changeform we set blank=True to avoid validation
    errors.
    """
    def __init__(self, *args, grouped_by=None, **kwargs):
        self.grouped_by = grouped_by
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class UsingReorderItemsSignalsMixin:
    """
    This mixin makes a integer field known by the signal handlers as a reorder
    items field. (See :mod:`~.signals` for more details.)

    To work fine with the logic of the signal handlers we set unique=False,
    since it is not possible to update indexes of a unique field without running
    into unique contraint violations.
    """
    def __init__(self, *args, grouped_by=None, **kwargs):
        self.grouped_by = grouped_by
        kwargs['unique'] = False
        super().__init__(*args, **kwargs)


class ReorderItemsField(
    UsingReorderItemsAdminMixin,
    UsingReorderItemsSignalsMixin,
    models.PositiveSmallIntegerField
):
    """
    A PositivSmallIntegerField using :class:`.UsingReorderItemsAdminMixin`
    and :class:`.UsingReorderItemsSignalsMixin`.
    """