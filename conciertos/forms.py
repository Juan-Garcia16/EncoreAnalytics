from django import forms
from django.utils import timezone
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

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        total_income = cleaned.get('total_income')
        start_dt = cleaned.get('start_datetime')

        # Only allow total_income when concert status is 'completed'
        if total_income not in (None, '') and status != 'completed':
            # attach error to the total_income field
            self.add_error('total_income', forms.ValidationError(
                'Solo puede registrar ingresos si el concierto está marcado como "Realizado".'
            ))

        # If the concert is marked as completed, ensure the start_datetime is not in the future.
        # i.e. you should not mark a concert as 'Realizado' if its date is after now.
        if status == 'completed' and start_dt:
            now = timezone.now()
            # allow a small tolerance (e.g., seconds) but generally ensure start_dt <= now
            if start_dt > now:
                self.add_error('status', forms.ValidationError(
                    'No se puede marcar como "Realizado" un concierto cuya fecha es futura.'
                ))

        return cleaned


