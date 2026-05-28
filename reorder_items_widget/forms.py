from django import forms
from .widgets import ReorderItemsWidget


class ReorderItemsFormField(forms.IntegerField):
    """
    Same as the forms.IntegerField, but using the
    :class:`~.widgets.ReorderItemsIndexWidget`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not issubclass(self.widget.__class__, ReorderItemsWidget):
            self.widget = ReorderItemsWidget()