from django.contrib import admin
from django.test import TestCase

from example.admin import ItemInline, BaseItemAdmin
from example.models import Container, Item
from reorder_items_widget.models import ReorderItemsField
from reorder_items_widget.widgets import ReorderItemsWidget

# Just for coverage score.
from reorder_items_widget import __version__


class WidgetTestCase(TestCase):
    def test_widget(self):
        widget = ReorderItemsWidget()
        css_classes = widget.build_attrs(dict(), dict())['class']
        self.assertIn('reorder-items-widget-index', css_classes)

    def test_rendering_with_value(self):
        widget = ReorderItemsWidget()
        html = widget.render('index', 1)
        input = '<input type="number" name="index" value="1" class="reorder-items-widget-index hidden">'
        drag_handle = '<div title="Drag me!" class="drag-handle">⇳</div>'
        self.assertInHTML(input, html)
        self.assertInHTML(drag_handle, html)

    def test_rendering_without_value(self):
        widget = ReorderItemsWidget()
        html = widget.render('index', None)
        input = '<input type="number" name="index" class="reorder-items-widget-index hidden">'
        drag_handle = '<div title="Drag me!" class="drag-handle">⇳</div>'
        self.assertInHTML(input, html)
        self.assertNotIn(drag_handle, html)


class ReorderItemsFieldTests(TestCase):
    def test_reorder_items_field_is_blank(self):
        field = Item._meta.get_field('index')
        self.assertTrue(field.blank)

    def test_reorder_items_field_formfield_uses_widget(self):
        field = Item._meta.get_field('index')
        form_field = field.formfield()
        self.assertIsInstance(form_field.widget, ReorderItemsWidget)

    def test_reorder_items_field_rejects_unique_true(self):
        with self.assertRaisesMessage(ValueError, 'Do not use unique=True with a ReorderItemsField.'):
            ReorderItemsField(unique=True)


class ReorderItemsSignalsTests(TestCase):
    fixtures = ['testdata.json']

    def test_pre_save_sets_next_index_for_new_item(self):
        container = Container.objects.get(pk=1)
        last_item = container.item_set.last()
        item = Item.objects.create(name='Item-Seven', container=container)

        self.assertEqual(item.index, last_item.index + 1)

    def test_post_delete_reorders_following_items(self):
        container = Container.objects.get(pk=1)
        original_indexes = list(container.item_set.all().values_list('index', flat=True))
        container.item_set.get(index=2).delete()
        new_indexes = list(container.item_set.all().values_list('index', flat=True))

        self.assertEqual(original_indexes[:-1], new_indexes)

    def test_signals_with_model_having_no_reorder_items_field(self):
        container = Container.objects.create(name='test-container')
        container.delete()


class ReorderItemsAdminTests(TestCase):
    def test_model_admin_mixin_includes_index_fields(self):
        admin_instance = BaseItemAdmin(Item, admin.site)

        self.assertIn('index', admin_instance.list_display)
        self.assertIn('index', admin_instance.exclude)
        self.assertIn('index', admin_instance.list_editable)

    def test_inline_mixin_includes_index_field(self):
        inline = ItemInline(Container, admin.site)

        self.assertIn('index', inline.fields)
