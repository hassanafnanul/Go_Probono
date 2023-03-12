from django import forms
from .models import UserWithRole

class UserWithRoleForm(forms.ModelForm):
    class Meta:
        model=UserWithRole
        fields=['picture']
