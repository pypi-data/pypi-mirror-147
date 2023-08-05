
from django import forms

from ckeditor.widgets import CKEditorWidget

from apps.callback.models import Callback


class CallbackForm(forms.ModelForm):

    class Meta:
        model = Callback
        fields = ('name', 'phone', 'descriptions')
        widgets = {
            'descriptions': CKEditorWidget
        }
