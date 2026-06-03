"""
Reorder your items by simply dragging them to their new position. This works
fine within admin changelists and inline formsets.

The main component is the :class:`~.widgets.ReorderItemsWidget` which provides
the drag and drop interface on top of an index field and updates the indexes of
listed items on form submission.

Still there are some neccessary setups to make a full functional admin
integration. Therefore we provide the :class:`~.models.ReorderItemsField` model
field, some :mod:`signal handlers <.signals>` and some :mod:`admin mixins
<.admin>` for your model admin or inline class. Using these components getting
you started with a minimal setup.

Just have a look at the :doc:`getting started <topics/getting_started>` section.
"""

from .widgets import *  # noqa
from .models import *  # noqa
from .admin import *  # noqa
