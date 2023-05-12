from django import forms
#from intl_tel_input.widgets import IntlTelInputWidget
from .models import *
from django.utils.html import format_html
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RequiredFileField(forms.FileField):
    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        contents = format_html('{}', self.label)
        attrs = attrs or {}
        attrs['for'] = self.widget.id_for_label(self.label)
        return format_html('<label{}>{}{}</label>', forms.utils.flatatt(attrs), contents, label_suffix)
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('document',)

        widgets = {
            'document': forms.FileInput(attrs={'required': True}),
        }

    def clean_document(self):
        document = self.cleaned_data.get('document')
        if not document:
            raise forms.ValidationError('You must upload a document.')
        return document

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

