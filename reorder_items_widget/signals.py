from django.db import models
from django.dispatch import receiver
from django.core.exceptions import FieldError
from .models import ReorderItemsFieldMixin


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
    # Ensure instance was added and not changed.
    if not instance.pk is None:
        return

    # Check if instance has a reorder items field.
    if not any([isinstance(f, ReorderItemsFieldMixin) for f in instance._meta.get_fields()]):
        return

    # Set the index to the next higher value.
    field = get_reorder_items_field(instance)
    items = get_items(instance)
    max_index = items.aggregate(models.Max(field.name))[f'{field.name}__max'] or -1
    setattr(instance, field.name, max_index + 1)



@receiver(models.signals.post_delete)
def post_delete_reorder_items(sender, instance, **kwargs):
    # Check if instance has a reorder items field.
    if not any([isinstance(f, ReorderItemsFieldMixin) for f in instance._meta.get_fields()]):
        return

    field = get_reorder_items_field(instance)
    items = get_items(instance)
    for item in items.filter(index__gt=getattr(instance, field.name)):
        item.index -= 1
        item.save()
