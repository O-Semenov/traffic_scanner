from django import forms
from .models import Scan


class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = ['path_file']
        widgets = {
            'path_file': forms.FileInput(attrs={'class' : 'form-control'}),
        }
