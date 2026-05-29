from django.contrib import admin

from .models import ReorderItemsField


class BaseReorderItemsAdminMixin:
    def get_reorder_items_field(self):
        fields = self.model._meta.get_fields()
        try:
            return next((f for f in fields if isinstance(f, ReorderItemsField)))
        except StopIteration:
            raise AttributeError(f'Model has not ReorderItemsField: {self.model}')


class ReorderItemsInlineMixin(BaseReorderItemsAdminMixin):
    """
    An inline mixin adding the name of the :class:`~.models.ReorderItemsField`
    to the `fields` attribute.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.get_reorder_items_field()

        # Update fields.
        self.fields = self.fields or tuple()
        if not field.name in self.fields:
            self.fields += (field.name,)


class ReorderItemsModelAdminMixin(BaseReorderItemsAdminMixin):
    """
    An inline mixin adding the name of the :class:`~.models.ReorderItemsField`
    to the `list_display`, `exclude` and `list_editable` attributes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.get_reorder_items_field()

        # Update list_display.
        self.list_display = self.list_display or tuple()
        if not field.name in self.list_display:
            self.list_display += (field.name,)

        # Update exclude.
        self.exclude = self.exclude or tuple()
        if not field.name in self.exclude:
            self.exclude += (field.name,)

        # Update list_editable.
        self.list_editable = self.list_editable or tuple()
        if not field.name in self.list_editable:
            self.list_editable += (field.name,)


class ReorderItemsModelAdmin(ReorderItemsModelAdminMixin, admin.ModelAdmin):
    """
    A model admin class using the :class:`~.ReorderItemsModelAdminMixin` mixin.
    """
    pass