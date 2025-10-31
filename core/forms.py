# core/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Artist
from .countries import get_countries
from .genres import get_genres

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'country', 'debut_year', 'genre']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary',
                'list': 'countries-list' # para el datalist
            }),
            'debut_year': forms.NumberInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
            'genre': forms.TextInput(attrs={
                'class': 'w-full bg-[#111722] border border-[#324467] text-white rounded-lg px-3 py-2 focus:ring-primary focus:border-primary'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer 'genre' requerido a nivel de formulario y conectar datalist
        self.fields['genre'].required = True
        self.fields['genre'].error_messages['required'] = 'El género es obligatorio.'
        # Asegurar que el widget incluya el atributo list para el datalist
        if 'list' not in self.fields['genre'].widget.attrs:
            self.fields['genre'].widget.attrs['list'] = 'genres-list'

    def clean_genre(self):
        genre = self.cleaned_data.get('genre', '')
        genre = genre.strip()
        # Validación case-insensitive contra la lista estática
        existing = {g.lower() for g in get_genres()}
        if genre.lower() not in existing:
            raise ValidationError('Seleccione un género válido de la lista.')
        return genre

    def clean_debut_year(self):
        year = self.cleaned_data.get('debut_year')
        try:
            year_int = int(year)
        except (TypeError, ValueError):
            raise ValidationError('Ingrese un año válido.')
        if year_int < 1950 or year_int > 2025:
            raise ValidationError('El año de debut debe estar entre 1950 y 2025.')
        return year_int

    def clean_country(self):
        country = self.cleaned_data.get('country', '')
        country = country.strip()
        # Obtener la lista de países desde helper (pycountry o fallback)
        existing = set(get_countries())
        if country not in existing:
            raise ValidationError('Seleccione un país válido de la lista.')
        return country
