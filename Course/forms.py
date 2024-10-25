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

class Media(forms.ModelForm):
    model = Profile
    fields = ['telegram_id',
              'building1_purchased',
              'building2_purchased',
              'building3_purchased',
              'building4_purchased']

    widgets = {
        'telegram_id': forms.TextInput(attrs={'class': 'form-control'}),
        'building1_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'building2_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'building3_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'building4_purchased': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
