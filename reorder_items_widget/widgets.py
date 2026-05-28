from django.forms import NumberInput


class ReorderItemsWidget(NumberInput):
    """
    Makes a number field a reorder items widget. Means the original field will
    be hidden and a drag handler will be displayed instead. Items in result
    lists and inline formsets will be reorderable by dragging the rows to their
    new position.
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
