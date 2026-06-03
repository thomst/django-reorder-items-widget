# Welcome to django-reorder-items-widget

[![Tests](https://github.com/thomst/django-reorder-items-widget/actions/workflows/tests.yml/badge.svg)](https://github.com/thomst/django-reorder-items-widget/actions/workflows/tests.yml)
[<img src="https://coveralls.io/repos/github/thomst/django-reorder-items-widget/badge.svg?branch=main">](https://coveralls.io/github/thomst/django-reorder-items-widget?branch=main)
[<img src="https://img.shields.io/badge/python-3-blue">](https://img.shields.io/badge/python-3-blue)
[<img src="https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange">](https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange)


## Links

- [github](https://github.com/thomst/django-reorder-items-widget/)
- [docs](https://thomst.github.io/django-reorder-items-widget/)
- [pypi](https://pypi.org/project/django-reorder-items-widget/)


## Description

Reorder your items by simply dragging them to their new position. This works
fine within admin changelists and inline formsets.

The main component is the [ReorderItemsWidget] which provides the drag and drop
interface on top of an index field and updates the indexes of listed items on
form submission.

Still there are some neccessary setups to make a full functional admin
integration of the reorder items feature: we need a [model field] for the
widget, an appropriate [admin configuration] and we probably do not want to
update indexes manually when adding or removing items bypassing the widget.
Therefore we use some [signal handlers] for the model field.

This app provides everything you need to make this setup as easy as possible.

[ReorderItemsWidget]: https://thomst.github.io/django-reorder-items-widget/topics/widgets.html
[model field]: https://thomst.github.io/django-reorder-items-widget/topics/models.html
[admin configuration]: https://thomst.github.io/django-reorder-items-widget/topics/admin.html
[signal handlers]: https://thomst.github.io/django-reorder-items-widget/topics/signals.html


## Installation

Install via pip:

```
pip install django-reorder-items-widget
```

Add `reorder_items_widget` to your `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    'reorder_items_widget',
    ...
]
```


## Getting started

### Setup for a reorderable changelist

Add a `ReorderItemsField` field to your model:

```
from django.db import models
from reorder_items_widget import ReorderItemsField

class Item(models.Model):
    ...
    index = models.ReorderItemsField()

    class Meta:
        ordering = ('index',)
```

Setup your model admin using the `ReorderItemsModelAdmin`:

```
from django.contrib import admin
from reorder_items_widget import ReorderItemsModelAdmin

class ItemModelAdmin(ReorderItemsModelAdmin):
    ...
```

You don't have to do anything with the index field in your model admin. It's
already setup by the base class.

Now you can reorder your items within the changelist only by drag and drop. And
completely forget about the index field which won't show up in the whole admin
backend at all.

### Setup for a reorderable inline

Again setup your models with a `ReorderItemsField`:

```
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
```

Mind the grouped_by argument for the `ReorderItemsField`. This argument tells
the field, that the ordering should be container specific. For each container
object the indexes of the related items will start anew with zero.

Now setup the model admins using the `ReorderItemsInline`:

```
from django.contrib import admin
from reorder_items_widget import ReorderItemsInline

class ItemInline(ReorderItemsInline):
    ...

class ContainerModelAdmin(admin.ModelAdmin):
    inlines = (ItemInline,)
```

Again there is no need to handle the index field.

Now visit the changeform of your container object and enjoy reordering its
items.


## Caveats

The widget will always number your items sequentially. So reordering a filtered
list of items might have unexpected results. Paging however should not be a
problem since the index of the first listed item will be used as a base.


## Contribute

Feedback, feature requests, bug reports or pull requests are most welcome. Just
use the common github infrastructure.
