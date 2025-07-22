# widgets.py
from collections.abc import Iterable
from typing import Any, Mapping
from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html, mark_safe


class CheckboxTextInput(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
                forms.CheckboxInput(attrs=attrs),
                forms.TextInput(attrs=attrs),
                ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None]

    def format_output(self, rendered_widgets):
        return f'{rendered_widgets[0]} {rendered_widgets[1]}'

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return ','.join(values)


class GroupedSelect(forms.Widget):
    def __init__(self, model, display_field, group_field, all_option=None, attrs=None, queryset=None):
        self.model = model
        self.display_field = display_field
        self.group_field = group_field
        self.all_option = all_option
        self._queryset = queryset # allows setting a filter on the model
        super().__init__(attrs)

    @property
    def queryset(self):
        # Lazy-load queryset when accessed
        if self._queryset is None:
            self._queryset = self.model.objects.all()
        return self._queryset
    
    def create_optgroups(self):
        groups = self.queryset.values_list(self.group_field, flat=True).distinct().order_by(self.group_field)
        optgroups = []
        for group in groups:
            options = self.queryset.filter(**{self.group_field: group}).values_list('id', self.display_field)
            optgroup = (group, [(id, display) for id, display in options], None)
            optgroups.append(optgroup)
        return optgroups

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        if attrs is None:
            attrs = {}
        attrs['name'] = name
        final_attrs = dict(attrs, name=name)
        output = [format_html('<select{}>', flatatt(final_attrs))]
        output.append(format_html('<option value=""></option>'))  # Add blank option
        for group_name, group_choices, _ in self.create_optgroups():
            output.append(format_html('<optgroup label="{}">', group_name))
            if self.all_option:
                output.append(format_html('<option value="{}-all" data-group="{}">Insert All</option>', group_name, group_name))
            for option_value, option_label in group_choices:
                selected_html = mark_safe(' selected="selected"') if str(option_value) == str(value) else ''
                output.append(format_html('<option value="{}" data-group="{}"{}>{}</option>', option_value, group_name, selected_html, option_label))
            output.append('</optgroup>')
        output.append('</select>')
        test = format_html(
            ''' 
            <script>
            $(document).ready(function() {{
                $("select[name='{}']").select2();
                $("select[name='{}']").on('select2:open', function () {{
                    $('.select2-dropdown').css('opacity', 0);
                    setTimeout(() => {{
                        $('.select2-container--open .select2-results__group').siblings().hide();
                        $('.select2-dropdown').css('opacity', 1);
                    }})
                }});
            }});
            </script>''', name, name)
        output.append(test)
        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)
