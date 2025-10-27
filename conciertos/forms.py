from django import forms
from .models import Concert, Tour
from core.models import Artist, Venue


class ConcertForm(forms.ModelForm):
    """Formulario para crear/editar Concert con estilo similar al form de Artista.

    El campo `artist` es un ModelChoiceField que sólo permite seleccionar
    artistas ya registrados (sin posibilidad de texto libre).
    """

    artist = forms.ModelChoiceField(
        queryset=Artist.objects.order_by('name'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary'
        })
    )

    venue = forms.ModelChoiceField(
        queryset=Venue.objects.order_by('name'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary'
        })
    )

    tour = forms.ModelChoiceField(
        queryset=Tour.objects.order_by('name'),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary'
        })
    )

    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary'
        })
    )

    status = forms.ChoiceField(
        choices=Concert._meta.get_field('status').choices,
        widget=forms.Select(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary'
        })
    )

    total_income = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary'
        })
    )

    img = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary',
            'placeholder': 'URL de imagen (opcional)'
        })
    )

    class Meta:
        model = Concert
        fields = ['artist', 'venue', 'tour', 'start_datetime', 'status', 'total_income', 'img']


