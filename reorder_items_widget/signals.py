"""
This module provides two signal handlers that works with a reorder items model
field. The field will be identified by the
:class:`UsingReorderItemsSignalsMixin` as its subclass.

The pre_save signal makes sure that the value of this field is set to the next
higher value when a new item is created. The post_delete signal fixes the values
of the remaining items when an item was deleted.

The items to deduce the next higher value or to fix will be filtered by the
fields listed in the `grouped_by` attribute of the field, if it is set.
Otherwise all items will be evaluated.
"""

from django.db import models
from django.dispatch import receiver
from django.core.exceptions import FieldError
from .models import ReorderItemsFieldMixin


def has_reorder_items_field(instance):
    fields = instance._meta.get_fields()
    return any([isinstance(f, ReorderItemsFieldMixin) for f in fields])


def get_reorder_items_field(instance):
    fields = instance._meta.get_fields()
    return next((f for f in fields if isinstance(f, ReorderItemsFieldMixin)), None)


def get_items(instance):
    reorder_items_field = get_reorder_items_field(instance)
    filter_keys = reorder_items_field.grouped_by or list()
    msg = f'Cannot resolve grouped_by values in model field attributes: {filter_keys}'
    try:
        filter_params = dict([(k, getattr(instance, k)) for k in filter_keys])
    except AttributeError:
        raise ValueError(msg)
    try:
        return instance._meta.model.objects.filter(**filter_params)
    except FieldError:
        raise ValueError(msg)


@receiver(models.signals.pre_save)
def pre_save_reorder_items(sender, instance, **kwargs):
    """
    A pre_save signal handler setting the :class:`ReorderItemsField` of a new
    item to the next higher value.
    """
    # Ensure instance was added and not changed.
    if not instance.pk is None:
        return

    # Check if instance has a reorder items field.
    if not has_reorder_items_field(instance):
        return

    # Set the index to the next higher value.
    field = get_reorder_items_field(instance)
    items = get_items(instance)
    max_index = items.aggregate(models.Max(field.name))[f'{field.name}__max'] or -1
    if getattr(instance, field.name) is None:
        setattr(instance, field.name, max_index + 1)



@receiver(models.signals.post_delete)
def post_delete_reorder_items(sender, instance, **kwargs):
    """
    A post_delete signal handler fixing the :class:`ReorderItemsField` values of
    remaining items.
    """
    # Check if instance has a reorder items field.
    if not has_reorder_items_field(instance):
        return

    field = get_reorder_items_field(instance)
    items = get_items(instance)
    index = getattr(instance, field.name)
    for item in items.filter(index__gt=index):
        item.index = index
        item.save()
        index += 1
