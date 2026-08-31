from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'civilite',
            'nom',
            'prenom',
            'email',
            'telephone',
            'mobile',
            'type_client',
            'budget',
            'notes',
        ]
        widgets = {
            'civilite': forms.TextInput(attrs={'placeholder': 'M., Mme, Dr...'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
