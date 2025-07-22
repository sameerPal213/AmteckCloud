# fields.py
from django import forms
from .widgets import CheckboxTextInput


class CheckboxTextField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = [
                forms.BooleanField(required=False),
                forms.CharField(required=False),
                ]
        super().__init__(fields, require_all_fields=False, *args, **kwargs)
        self.widget = CheckboxTextInput()

    def compress(self, data_list):
        return ','.joing(map(str, data_list))
