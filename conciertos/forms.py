from django import forms
from django.utils import timezone
from .models import Concert, Tour
from core.models import Artist, Venue
from .models import SetlistEntry, Song


class TourForm(forms.ModelForm):
    artist = forms.ModelChoiceField(
        queryset=Artist.objects.order_by('name'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'
        })
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'
        })
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'
        })
    )
    
    class Meta:
        model = Tour
        fields = ['artist', 'name', 'start_date', 'end_date', 'status', 'total_income']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'}),
            'status': forms.Select(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'}),
            'total_income': forms.NumberInput(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'}),
        }

    # asegurarse de que los ingresos no sean negativos a nivel de formulario
    total_income = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'})
    )

    # Validar coherencia entre fechas y estado de la gira
    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        status = cleaned.get('status')
        today = timezone.now().date()

        # Si se proporcionan ambas fechas, asegúrese de que end >= start
        if start and end:
            if end < start:
                self.add_error('end_date', forms.ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio.'))

            #ahora comprobar la coherencia del estado con el intervalo de fechas
            if end < today:
                # gira terminada en el pasado
                if status != 'finished':
                    self.add_error('status', forms.ValidationError('La gira finalizó en el pasado, el estado debería ser "Finalizada".'))
            elif start > today:
                # gira completamente en el futuro
                if status != 'planned':
                    self.add_error('status', forms.ValidationError('La gira comienza en el futuro, el estado debería ser "Planificada".'))
            else:
                # gira en curso
                if status != 'ongoing':
                    self.add_error('status', forms.ValidationError('La gira está en curso según las fechas, el estado debería ser "En curso".'))

        #si solo se proporciona la fecha inicio, comprobar estados plausibles
        elif start and not end:
            if start > today and status and status != 'planned':
                self.add_error('status', forms.ValidationError('La gira comienza en el futuro; use el estado "Planificada".'))

        # Si solo se proporciona la fecha de finalización, comprobar estados plausibles
        elif end and not start:
            if end < today and status and status != 'finished':
                self.add_error('status', forms.ValidationError('La fecha de finalización es pasada; el estado debería ser "Finalizada".'))

        return cleaned


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
        min_value=0,
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
        
    # Validar coherencia entre estado y total_income
    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        total_income = cleaned.get('total_income')
        start_dt = cleaned.get('start_datetime')

        # solo permitir total_income cuando el estado del concierto es 'realizado'
        if total_income not in (None, '') and status != 'completed':
            # así el error aparece junto al campo en el formulario
            self.add_error('total_income', forms.ValidationError(
                'Solo puede registrar ingresos si el concierto está marcado como "Realizado".'
            ))

        # si el concierto está marcado como realizado, asegúrese de que start_datetime no esté en el futuro.
        # i.e. no se debe marcar un concierto como 'Realizado' si su fecha es posterior a ahora.
        if status == 'completed' and start_dt:
            now = timezone.now()
            # permitir una pequeña tolerancia (por ejemplo, segundos) pero en general asegurarse de que start_dt <= now
            if start_dt > now:
                self.add_error('status', forms.ValidationError(
                    'No se puede marcar como "Realizado" un concierto cuya fecha es futura.'
                ))

        return cleaned


class SetlistEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # aceptar un kwarg `concert` para validar la unicidad de `position` dentro de ese concierto
        self._concert = kwargs.pop('concert', None)
        super().__init__(*args, **kwargs)
        # si el formulario se instanció con una instancia, asegurarse de tener el concierto
        if not self._concert and hasattr(self, 'instance') and getattr(self.instance, 'concert', None):
            self._concert = self.instance.concert

    class Meta:
        model = SetlistEntry
        fields = ['song', 'position', 'section', 'is_cover']
        widgets = {
            'song': forms.Select(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'}),
            'position': forms.NumberInput(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'}),
            'section': forms.TextInput(attrs={'class': 'form-input h-14 w-full rounded-lg bg-[#232f48] p-4 text-white'}),
            'is_cover': forms.CheckboxInput(attrs={'class': 'ml-2'}),
        }

        # Validar unicidad de `position` dentro del concierto
        def clean_position(self):
            pos = self.cleaned_data.get('position')
            if pos is None:
                return pos

            concert = self._concert
            if not concert:
                # si no conocemos el concierto aún, omitir la verificación de unicidad (la vista debería pasar el concierto)
                return pos

            # Validar unicidad de `song` dentro del concierto
            def clean_song(self):
                song = self.cleaned_data.get('song')
                if not song:
                    return song

                concert = self._concert
                if not concert:
                    # Si no conocemos el concierto aún, omitir la verificación de unicidad (la vista debería pasar el concierto)
                    return song

                # Verificar si la canción ya está en el setlist para este concierto
                qs = SetlistEntry.objects.filter(concert=concert, song=song)
                if self.instance and self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise forms.ValidationError('Esta canción ya está en el setlist para este concierto.')
                return song

            qs = SetlistEntry.objects.filter(concert=concert, position=pos)
            # excluir self al editar
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe una canción en esa posición para este concierto.')
            return pos


