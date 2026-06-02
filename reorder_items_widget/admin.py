from django.contrib import admin

from .models import UsingReorderItemsAdminMixin
from .widgets import ReorderItemsWidget


__all__ = (
    'ReorderItemsInlineMixin',
    'ReorderItemsInline',
    'ReorderItemsModelAdminMixin',
    'ReorderItemsModelAdmin',
)


class GetReorderItemsFieldMixin:
    """
    A mixin to get the reorder items field from the model.
    """
    def get_reorder_items_field(self):
        fields = self.model._meta.get_fields()
        try:
            return next((f for f in fields if isinstance(f, UsingReorderItemsAdminMixin)))
        except StopIteration:
            raise AttributeError(f'Model has not ReorderItemsField: {self.model}')


class ReorderItemsInlineMixin(GetReorderItemsFieldMixin):
    """
    An inline mixin adding the name of the :class:`~.models.ReorderItemsField`
    to the `fields` attribute. Use this mixin with a TabularInline since this is
    what the :class:`~.widgets.ReorderItemsWidget` was designed for.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.get_reorder_items_field()

        # Update formfield_overwrites.
        self.formfield_overrides = self.formfield_overrides or dict()
        self.formfield_overrides[type(field)] = dict(widget=ReorderItemsWidget())

        # Update fields.
        self.fields = self.fields or tuple()
        if not field.name in self.fields:
            self.fields += (field.name,)


class ReorderItemsModelAdminMixin(GetReorderItemsFieldMixin):
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

    def get_changelist_form(self, request, **kwargs):
        form = super().get_changelist_form(request, **kwargs)
        field = self.get_reorder_items_field()
        meta = getattr(form, 'Meta', type('Meta', (), dict()))
        meta.widgets = getattr(meta, 'widgets', None) or dict()
        meta.widgets[field.name] = ReorderItemsWidget()
        return type(form.__name__, (form,), dict(Meta=meta))


class ReorderItemsInline(ReorderItemsInlineMixin, admin.TabularInline):
    """
    A TabularInline using the :class:`.ReorderItemsInlineMixin`.
    """


class ReorderItemsModelAdmin(ReorderItemsModelAdminMixin, admin.ModelAdmin):
    """
    A model admin class using the :class:`~.ReorderItemsModelAdminMixin` mixin.
    """
    pass