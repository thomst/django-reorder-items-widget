from django.db import models
from reorder_items_widget.models import ReorderItemsField


class Container(models.Model):
    """
    Simple container for items.
    """
    name = models.CharField('Name', max_length=255)


class BaseItem(models.Model):
    """
    Base for simple item models with an index for ordering.
    """
    name = models.CharField('Name', max_length=255)
    index = ReorderItemsField(grouped_by=['container'])
    container = models.ForeignKey(Container, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ('container', 'index')


class Item(BaseItem):
    """
    Simple item with an index for ordering.
    """


class AnotherItem(BaseItem):
    """
    Another simple item with an index for ordering.
    """
