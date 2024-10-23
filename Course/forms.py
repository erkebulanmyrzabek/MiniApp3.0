from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telegram_id',
                  'username',
                  'coin']

        widgets = {
            'telegram_id': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'coin': forms.TextInput(attrs={'class': 'form-control'}),
        }