from django import forms
from trello.models import Workspace

class SampleForm(forms.Form):
    testing_choices = (
            ("1", "Testing1"),
            ("2", "Testing2"),
            )
    TextInput = forms.CharField(label="Name", max_length=100, widget=forms.TextInput)
    NumberInput = forms.CharField(label="Name", max_length=100, widget=forms.NumberInput)
    EmailInput = forms.CharField(label="Name", max_length=100, widget=forms.EmailInput)
    URLInput = forms.CharField(label="Name", max_length=100, widget=forms.URLInput)
    PasswordInput = forms.CharField(label="Name", max_length=100, widget=forms.PasswordInput)
    HiddenInput = forms.CharField(label="Name", max_length=100, widget=forms.HiddenInput)
    DateInput = forms.CharField(label="Name", max_length=100, widget=forms.DateInput)
    DateTimeInput = forms.CharField(label="Name", max_length=100, widget=forms.DateTimeInput)
    TimeInput = forms.CharField(label="Name", max_length=100, widget=forms.TimeInput)
    Textarea = forms.CharField(label="Name", max_length=100, widget=forms.Textarea)
    TestBooelan = forms.BooleanField()
    ChoiceField = forms.ChoiceField(choices=testing_choices)
    DateField   = forms.DateField()
    DateTime    = forms.DateTimeField()
    DecimalField    = forms.DecimalField()
    DurationField   = forms.DurationField()
    EmailField      = forms.EmailField()
    FileField       = forms.FileField()
    FilePathField   = forms.FilePathField(path='/')
    FloatFiled      = forms.FloatField()
    GenericIPAddressField = forms.GenericIPAddressField()
    ImageField      = forms.ImageField()
    IntegerField    = forms.IntegerField()
    JSONField       = forms.JSONField()
    MultipleChoiceField = forms.MultipleChoiceField(choices=testing_choices)
    NullBooleanField    = forms.NullBooleanField()
    RegexField      = forms.RegexField(regex="")
    SlugField       = forms.SlugField()
    TimeField       = forms.TimeField()
    TypedChoiceField    = forms.TypedChoiceField(
            choices=testing_choices,
            coerce=int(),
            empty_value='')
    TypedMultipleChoiceField    = forms.TypedMultipleChoiceField(
            choices=testing_choices,
            coerce=int(),
            empty_value='')
    URLField    = forms.URLField()
    UUIDField   = forms.UUIDField()
    ComboField  = forms.ComboField(fields=[forms.CharField(max_length=20),
        forms.EmailField()])
    SplitDateTimeField  = forms.SplitDateTimeField()
    ModelChoiceField    = forms.ModelChoiceField(queryset=Workspace.objects.all())
    ModelMultipleChoiceField    = forms.ModelMultipleChoiceField(
            queryset=Workspace.objects.all(),
            help_text='This is a test of the help text')
