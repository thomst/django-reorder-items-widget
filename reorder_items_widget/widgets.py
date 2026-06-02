from django.forms import NumberInput


__all__ = (
    'ReoroderItemsWidgetMixin',
    'ReorderItemsWidget',
)


class ReoroderItemsWidgetMixin:
    """
    Widget to make a number input a reorder items widget. The original form
    field will be hidden and a drag and drop handler will be rendered instead.
    Items in result lists and inline formsets will be reorderable by dragging
    the rows to their new position.

    On form submission the index values will be updated to reflect the new
    order.
    """
    template_name = 'forms/widgets/reorder-items-widget.html'

    class Media:
        css = {'all': ('css/reorder-items-widget.css',)}
        js = ('js/reorder-items-widget.js',)

    def build_attrs(self, base_attrs, extra_attrs):
        """
        Add the CSS classes for the widget.
        """
        attrs = super().build_attrs(base_attrs, extra_attrs)
        classes = attrs['class'].split(' ') if attrs.get('class') else []
        classes += ['reorder-items-widget-index', 'hidden']
        attrs['class'] = ' '.join(classes)
        return attrs


class ReorderItemsWidget(ReoroderItemsWidgetMixin, NumberInput):
    """
    A NumberInput widget using the :class:`.ReoroderItemsWidgetMixin`.
    """
