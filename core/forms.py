# core/forms.py
from django import forms
from .models import Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'country', 'debut_year', 'genre']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
            'debut_year': forms.NumberInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
            'genre': forms.TextInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
        }
