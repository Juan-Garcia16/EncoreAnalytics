from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Tour, Concert, Song, SetlistEntry
from django.utils.decorators import method_decorator
from core.models import Artist
from .forms import ConcertForm, SetlistEntryForm, TourForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q, Max, Avg, Count
import json
from django.views.generic import DetailView
from django.db import IntegrityError
# ----- GIRA -----
class TourListView(ListView):
    model = Tour
    template_name = 'conciertos/tour_list.html'
    context_object_name = 'tours'
    queryset = Tour.objects.all().order_by('start_date')

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('query', '').strip()
        status = self.request.GET.get('status', '').strip()
        # Filtrar por nombre de artista si se proporciona una query
        if q:
            # buscar por nombre de artista O nombre de la gira (contiene, insensible a mayúsculas)
            qs = qs.filter(
                Q(artist__name__icontains=q) | Q(name__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_field = Tour._meta.get_field('status')
        context['status_choices'] = status_field.choices
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_query'] = self.request.GET.get('query', '').strip()
    # computar marcadores de posición para que la cuadrícula mantenga columnas consistentes en pantallas más grandes
        total = context.get('object_list').count() if context.get('object_list') is not None else 0
    # número de columnas en pantallas grandes es 3; computar cuántos espacios vacíos agregar
        remainder = total % 3
        placeholder_count = (3 - remainder) % 3
        context['placeholders'] = list(range(placeholder_count))
        return context


@method_decorator(staff_member_required, name='dispatch')
class TourCreateView(CreateView):
    model = Tour
    form_class = TourForm
    template_name = 'conciertos/tour_form.html'
    success_url = reverse_lazy('tour_list')


class TourDetailView(DetailView):
    model = Tour
    template_name = 'conciertos/tour_detail.html'
    context_object_name = 'tour'


@method_decorator(staff_member_required, name='dispatch')
class TourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    template_name = 'conciertos/tour_form.html'
    success_url = reverse_lazy('tour_list')


def tour_delete(request, pk):
    """Delete a tour. POST only."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    tour = get_object_or_404(Tour, pk=pk)
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('tour_list')
    tour.delete()
    return redirect('tour_list')
    tour.delete()
    return redirect('tour_list')

# ----- CONCIERTO -----
class ConcertListView(ListView):
    model = Concert
    template_name = 'conciertos/concert_list.html'
    context_object_name = 'concerts'
    queryset = Concert.objects.all().order_by('artist__name')
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('query_concerts', '').strip()
        status = self.request.GET.get('status', '').strip()
        if q:
            # Buscar por Artista, venue
            qs = qs.filter(
                Q(artist__name__icontains=q)
                | Q(venue__name__icontains=q)
                | Q(venue__city__name__icontains=q)
                | Q(venue__city__country__icontains=q)
            ).order_by('start_datetime')
        # Filtrar por estado si se pasa en la querystring
        if status:
            qs = qs.filter(status=status)
    # anotar con la calificación promedio y el recuento de calificaciones
        qs = qs.annotate(avg_rating=Avg('attendees__rating'), ratings_count=Count('attendees__rating'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasar opciones de estado al template (value, label)
        status_field = Concert._meta.get_field('status')
        context['status_choices'] = status_field.choices
        context['selected_status'] = self.request.GET.get('status', '')
        # Si el usuario está autenticado y tiene perfil de Fan, precomputar los conciertos en los que está interesado
        user = self.request.user
        user_interested_ids = []
        if user.is_authenticated:
            try:
                fan = user.fan
            except Exception:
                fan = None
            if fan:
                qs = context.get('concerts') or self.get_queryset()
                # importar aquí para evitar importaciones circulares en la carga del módulo
                from fans.models import Interest
                user_interested_ids = list(Interest.objects.filter(fan=fan, concert__in=qs).values_list('concert_id', flat=True))
                # calificaciones existentes del usuario para los conciertos mostrados
                from fans.models import Attendance
                user_attendances = Attendance.objects.filter(fan=fan, concert__in=qs).values_list('concert_id', 'rating')
                # mapear concert_id -> rating
                user_ratings = {c: r for c, r in user_attendances}
                context['user_ratings'] = user_ratings
                # también proporcionar JSON para la inicialización del lado del cliente
                context['user_ratings_json'] = json.dumps(user_ratings)
        context['user_interested_ids'] = user_interested_ids
        return context


class ConcertDetailView(DetailView):
    model = Concert
    template_name = 'conciertos/concert_detail.html'
    context_object_name = 'concert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        concert = self.get_object()
        # aggregate ratings
        agg = concert.attendees.filter(rating__isnull=False).aggregate(avg=Avg('rating'), count=Count('pk'))
        context['avg_rating'] = agg['avg'] or 0
        context['ratings_count'] = agg['count'] or 0
        # user's rating if any
        user = self.request.user
        user_rating = None
        if user.is_authenticated:
            try:
                fan = user.fan
                att = fan.attendances.filter(concert=concert).first()
                if att:
                    user_rating = att.rating
            except Exception:
                user_rating = None
        context['user_rating'] = user_rating
        return context

class ConcertCreateView(CreateView):
    model = Concert
    form_class = ConcertForm
    template_name = 'conciertos/concert_form.html'
    success_url = reverse_lazy('concert_list')

class ConcertUpdateView(UpdateView):
    model = Concert
    form_class = ConcertForm
    template_name = 'conciertos/concert_form.html'
    success_url = reverse_lazy('concert_list')

def concert_delete(request, pk):
    """Delete a concert. Accepts POST only and redirects to concert list."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    concert = get_object_or_404(Concert, pk=pk)
    # opcional: restringir eliminación a usuarios staff
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('concert_list')
    concert.delete()
    return redirect('concert_list')

# ----- SONG -----
class SongListView(ListView):
    model = Song
    template_name = 'conciertos/song_list.html'
    context_object_name = 'songs'
    queryset = Song.objects.all().order_by('title')

class SongCreateView(CreateView):
    model = Song
    fields = ['title', 'original_artist', 'release_year']
    template_name = 'conciertos/song_form.html'
    success_url = reverse_lazy('song_list')

# ----- SETLIST ENTRY -----
class SetlistEntryListView(ListView):
    model = SetlistEntry
    template_name = 'conciertos/setlistentry_list.html'
    context_object_name = 'setlist_entries'

class SetlistEntryCreateView(CreateView):
    model = SetlistEntry
    fields = ['concert', 'song', 'position', 'section', 'is_cover']
    template_name = 'conciertos/setlistentry_form.html'
    success_url = reverse_lazy('setlistentry_list')


def concert_setlist(request, pk):
    """Vista para mostrar las entradas del setlist de un solo concierto."""
    concert = get_object_or_404(Concert, pk=pk)
    entries = SetlistEntry.objects.filter(concert=concert).order_by('position')
    return render(request, 'conciertos/setlistentry_list.html', {'setlist_entries': entries, 'concert': concert})


@staff_member_required
def setlist_entry_add(request, concert_pk):
    """Vista solo para personal autorizado que permite agregar una entrada al setlist de un concierto."""
    concert = get_object_or_404(Concert, pk=concert_pk)
    # si no hay entradas, sugerir posición 1
    max_pos = SetlistEntry.objects.filter(concert=concert).aggregate(Max('position'))['position__max'] or 0
    suggested_position = max_pos + 1
    if request.method == 'POST':
        form = SetlistEntryForm(request.POST, concert=concert)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.concert = concert
            try:
                entry.save()
            except IntegrityError as err:
                # Determinar si el conflicto se debe a canción duplicada o posición duplicada
                # comprobando filas existentes en la base de datos en lugar de analizar mensajes específicos del motor.
                conflict_song_qs = SetlistEntry.objects.filter(concert=concert, song=entry.song)
                conflict_pos_qs = SetlistEntry.objects.filter(concert=concert, position=entry.position)
                # excluirse a sí mismo (no necesario al añadir pero inofensivo)
                if entry.pk:
                    conflict_song_qs = conflict_song_qs.exclude(pk=entry.pk)
                    conflict_pos_qs = conflict_pos_qs.exclude(pk=entry.pk)

                if conflict_song_qs.exists():
                    form.add_error('song', 'La canción ya está en el setlist para este concierto.')
                elif conflict_pos_qs.exists():
                    form.add_error('position', 'Ya existe una canción en esa posición para este concierto.')
                else:
                    # Error genérico por defecto
                    form.add_error(None, 'Error al guardar la entrada del setlist.')
                artists = Artist.objects.order_by('name')
                return render(request, 'conciertos/setlistentry_form.html', {'form': form, 'concert': concert, 'artists': artists, 'suggested_position': suggested_position})
            return redirect('concert_setlist', pk=concert.pk)
    else:
        form = SetlistEntryForm(concert=concert, initial={'position': suggested_position})
    artists = Artist.objects.order_by('name')
    return render(request, 'conciertos/setlistentry_form.html', {'form': form, 'concert': concert, 'artists': artists, 'suggested_position': suggested_position})


@staff_member_required
def setlist_entry_edit(request, pk):
    """Vista solo para personal autorizado para editar una entrada de setlist existente."""
    entry = get_object_or_404(SetlistEntry, pk=pk)
    concert = entry.concert
    if request.method == 'POST':
        form = SetlistEntryForm(request.POST, instance=entry, concert=concert)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError as err:
                # determinar el tipo de conflicto comprobando filas existentes
                inst = form.instance
                conflict_song_qs = SetlistEntry.objects.filter(concert=concert, song=inst.song).exclude(pk=inst.pk)
                conflict_pos_qs = SetlistEntry.objects.filter(concert=concert, position=inst.position).exclude(pk=inst.pk)
                if conflict_song_qs.exists():
                    form.add_error('song', 'La canción ya está en el setlist para este concierto.')
                elif conflict_pos_qs.exists():
                    form.add_error('position', 'Ya existe una canción en esa posición para este concierto.')
                else:
                    form.add_error(None, 'Error al guardar la entrada del setlist.')
                artists = Artist.objects.order_by('name')
                # sugeririr la siguiente posición disponible
                max_pos = SetlistEntry.objects.filter(concert=concert).aggregate(Max('position'))['position__max'] or 0
                suggested_position = max_pos + 1
                return render(request, 'conciertos/setlistentry_form.html', {'form': form, 'concert': concert, 'entry': entry, 'artists': artists, 'suggested_position': suggested_position})
            return redirect('concert_setlist', pk=concert.pk)
    else:
        form = SetlistEntryForm(instance=entry, concert=concert)
    artists = Artist.objects.order_by('name')
    max_pos = SetlistEntry.objects.filter(concert=concert).aggregate(Max('position'))['position__max'] or 0
    suggested_position = max_pos + 1
    return render(request, 'conciertos/setlistentry_form.html', {'form': form, 'concert': concert, 'entry': entry, 'artists': artists, 'suggested_position': suggested_position})


@staff_member_required
@require_http_methods(['POST'])
def setlist_entry_delete(request, pk):
    """Eliminación (solo staff) de una entrada del setlist. Acepta solo POST."""
    entry = get_object_or_404(SetlistEntry, pk=pk)
    concert_pk = entry.concert.pk
    entry.delete()
    return redirect('concert_setlist', pk=concert_pk)


@staff_member_required
@require_http_methods(['POST'])
def song_create_ajax(request):
    """Endpoint AJAX para crear una Song desde el formulario de setlist.

    Espera POST con 'title' (requerido), opcional 'original_artist' y 'release_year'.
    Devuelve JSON con el id y título de la canción creada.
    """
    title = request.POST.get('title', '').strip()
    original_artist = request.POST.get('original_artist', '').strip()
    release_year = request.POST.get('release_year', '').strip()

    errors = {}
    if not title:
        errors['title'] = 'El título es obligatorio.'

    # Validar release_year si se proporciona
    if release_year:
        try:
            release_year_int = int(release_year)
            if release_year_int < 0:
                raise ValueError()
        except ValueError:
            errors['release_year'] = 'Año inválido.'
    else:
        release_year_int = None

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # Intentar resolver original_artist a una instancia de Artist por nombre exacto; si no se encuentra,
    # almacenar el nombre proporcionado en `original_artist_name` (no creamos nuevas filas en Artist).
    artist_obj = None
    artist_name_to_store = None
    if original_artist:
        try:
            artist_obj = Artist.objects.get(name__iexact=original_artist)
        except Artist.DoesNotExist:
            artist_obj = None
            artist_name_to_store = original_artist

    song = Song.objects.create(
        title=title,
        original_artist=artist_obj,
        original_artist_name=artist_name_to_store,
        release_year=release_year_int,
    )

    return JsonResponse({'success': True, 'song': {'id': song.pk, 'title': song.title}})

