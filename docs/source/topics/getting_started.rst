Getting started
===============

Installation
------------

Install via pip::

    pip install django-reorder-items-widget

Add ``reorder_items_widget`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'reorder_items_widget',
        ...
    ]


Getting started
---------------

Setup for a reorderable changelist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add a ``ReorderItemsField`` field to your model::

    from django.db import models
    from reorder_items_widget import ReorderItemsField

    class Item(models.Model):
        ...
        index = models.ReorderItemsField()

        class Meta:
            ordering = ('index',)

Setup your model admin using the ``ReorderItemsModelAdmin``::

    from django.contrib import admin
    from reorder_items_widget import ReorderItemsModelAdmin

    class ItemModelAdmin(ReorderItemsModelAdmin):
        ...

You don't have to do anything with the index field in your model admin. It's
already setup by the base class.

Now you can reorder your items within the changelist only by drag and drop. And
completely forget about the index field which won't show up in the whole admin
backend at all.


Setup for a reorderable inline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Again setup your models with a ``ReorderItemsField``::

    from django.db import models
    from reorder_items_widget import ReorderItemsField

    class Container(models.Model):
        ...

    class Item(models.Model):
        ...
        index = models.ReorderItemsField(grouped_by=['container'])
        container = models.ForeignKey(Container, on_delete=models.CASCADE)

        class Meta:
            ordering = ('container', 'index')

Mind the ``grouped_by`` argument for the ``ReorderItemsField``. This argument tells
the field that the ordering should be container specific. For each container
object the indexes of the related items will start anew with zero.

Now setup the model admins using the ``ReorderItemsInline``::

    from django.contrib import admin
    from reorder_items_widget import ReorderItemsInline

    class ItemInline(ReorderItemsInline):
        ...

    class ContainerModelAdmin(admin.ModelAdmin):
        inlines = (ItemInline,)

Again there is no need to handle the index field.

Now visit the changeform of your container object and enjoy reordering its
items.
