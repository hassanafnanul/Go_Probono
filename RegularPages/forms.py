from django import forms
from .models import RegularPage
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget 

class RegularPagesForm(forms.ModelForm):
    # description = forms.CharField(widget=CKEditorUploadingWidget())
    description = forms.CharField(widget=CKEditorWidget('full'))

    class Meta:
        model = RegularPage
        fields = ('description',)

