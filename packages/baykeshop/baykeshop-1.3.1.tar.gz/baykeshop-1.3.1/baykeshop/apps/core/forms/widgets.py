from django.utils.translation import gettext_lazy as _
from django.forms import widgets


class Widget(widgets.Widget):
    pass


class Input(widgets.Input):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['class'] = 'input'


class TextInput(Input):
    input_type = "text"
    template_name = "django/forms/widgets/text.html"
