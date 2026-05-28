from django.contrib import admin
from reorder_items_widget.admin import ReorderItemsModelAdminMixin, ReorderItemsInlineMixin
from .models import Container, Item, AnotherItem


class BaseItemAdmin(ReorderItemsModelAdminMixin, admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Item)
class ItemAdmin(BaseItemAdmin):
    pass


@admin.register(AnotherItem)
class AnotherItemAdmin(BaseItemAdmin):
    pass


class BaseItemInline(ReorderItemsInlineMixin, admin.TabularInline):
    extra = 1
    fields = ("name",)


class ItemInline(BaseItemInline):
    model = Item


class AnotherItemInline(BaseItemInline):
    model = AnotherItem


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (ItemInline, AnotherItemInline)
