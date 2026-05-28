from django.apps import AppConfig


class ReorderItemsWidgetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reorder_items_widget'

    def ready(self):
        import reorder_items_widget.signals
