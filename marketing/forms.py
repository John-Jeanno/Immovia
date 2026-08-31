from __future__ import annotations

from django import forms

from .models import Annonce, CampagneMarketing, EmailMarketing, PublicationSociale


class CampagneForm(forms.ModelForm):
    class Meta:
        model = CampagneMarketing
        fields = ['nom']


class EmailMarketingForm(forms.ModelForm):
    class Meta:
        model = EmailMarketing
        fields = ['campagne', 'sujet', 'corps']


class PublicationSocialeForm(forms.ModelForm):
    class Meta:
        model = PublicationSociale
        fields = ['campagne', 'contenu']


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['campagne', 'titre', 'description']


class AnnonceFormSet(forms.BaseInlineFormSet):
    """Formset minimal compatible avec les imports historiques."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
