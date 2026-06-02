from django.db import models


__all__ = (
    'ReorderItemsFieldMixin',
    'ReorderItemsField',
)


class ReorderItemsFieldMixin:
    """
    This mixin makes an integer field known by the signal handlers and the admin
    classes as a reorder items field. (See :mod:`~.signals` and :mod:`~.admin`
    for more details.)

    To work fine with the logic of the signal handlers we set `unique=False`,
    since it is not possible to update indexes of a unique field without running
    into unique contraint violations.

    And since :class:`~.admin.ReorderItemsModelAdminMixin` excludes the reorder
    items field from the changeform we set blank=True to avoid validation
    errors. The value will be set by the pre_save signal handler when a new item
    is created.

    There is an additional keyword argument `grouped_by` that can be used to
    specify a list of field names to group the items by. This is useful to make
    items reorderable in an inline context, where the order of the items should
    be specific to the related model. Here is a simple example to illustrate
    such a use case::


        class Blog(models.Model):
            name = models.CharField(max_length=100)


        class Article(models.Model):
            index = ReorderItemsField(grouped_by=['blog'])
            blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
            text = models.TextField()

            class Meta:
                ordering = ('blog', 'index')
    """
    def __init__(self, *args, grouped_by=None, **kwargs):
        self.grouped_by = grouped_by
        kwargs['unique'] = False
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class ReorderItemsField(ReorderItemsFieldMixin, models.PositiveSmallIntegerField):
    """
    A PositivSmallIntegerField using :class:`.ReorderItemsFieldMixin`.
    """