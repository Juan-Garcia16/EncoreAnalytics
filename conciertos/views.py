from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Tour, Concert, Song, SetlistEntry
from core.models import Artist
from .forms import ConcertForm, SetlistEntryForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q, Max
from django.db import IntegrityError
# Create your views here.

# ----- TOUR -----
class TourListView(ListView):
    model = Tour
    template_name = 'conciertos/tour_list.html'
    context_object_name = 'tours'

class TourCreateView(CreateView):
    model = Tour
    fields = ['artist', 'name', 'start_date', 'end_date', 'status', 'total_income']
    template_name = 'conciertos/tour_form.html'
    success_url = reverse_lazy('tour_list')

# ----- CONCERT -----
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
                # import here to avoid circular-imports at module load
                from fans.models import Interest
                user_interested_ids = list(Interest.objects.filter(fan=fan, concert__in=qs).values_list('concert_id', flat=True))
        context['user_interested_ids'] = user_interested_ids
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
    # Optional: restrict deletion to staff users
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
    """View to display the setlist entries for a single concert."""
    concert = get_object_or_404(Concert, pk=pk)
    entries = SetlistEntry.objects.filter(concert=concert).order_by('position')
    return render(request, 'conciertos/setlistentry_list.html', {'setlist_entries': entries, 'concert': concert})


@staff_member_required
def setlist_entry_add(request, concert_pk):
    """Staff-only view to add a SetlistEntry to a concert."""
    concert = get_object_or_404(Concert, pk=concert_pk)
    # compute suggested next position (max position + 1)
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
                # Determine whether the conflict is due to duplicate song or duplicate position
                # by checking existing rows in the DB rather than parsing DB-specific messages.
                conflict_song_qs = SetlistEntry.objects.filter(concert=concert, song=entry.song)
                conflict_pos_qs = SetlistEntry.objects.filter(concert=concert, position=entry.position)
                # exclude self (not needed for add but harmless)
                if entry.pk:
                    conflict_song_qs = conflict_song_qs.exclude(pk=entry.pk)
                    conflict_pos_qs = conflict_pos_qs.exclude(pk=entry.pk)

                if conflict_song_qs.exists():
                    form.add_error('song', 'La canción ya está en el setlist para este concierto.')
                elif conflict_pos_qs.exists():
                    form.add_error('position', 'Ya existe una canción en esa posición para este concierto.')
                else:
                    # Fallback generic error
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
    """Staff-only view to edit an existing SetlistEntry."""
    entry = get_object_or_404(SetlistEntry, pk=pk)
    concert = entry.concert
    if request.method == 'POST':
        form = SetlistEntryForm(request.POST, instance=entry, concert=concert)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError as err:
                # determine conflict type by checking existing rows
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
                # compute suggested next position for display (useful when editing)
                max_pos = SetlistEntry.objects.filter(concert=concert).aggregate(Max('position'))['position__max'] or 0
                suggested_position = max_pos + 1
                return render(request, 'conciertos/setlistentry_form.html', {'form': form, 'concert': concert, 'entry': entry, 'artists': artists, 'suggested_position': suggested_position})
            return redirect('concert_setlist', pk=concert.pk)
    else:
        form = SetlistEntryForm(instance=entry, concert=concert)
    artists = Artist.objects.order_by('name')
    # compute suggested position for display when editing
    max_pos = SetlistEntry.objects.filter(concert=concert).aggregate(Max('position'))['position__max'] or 0
    suggested_position = max_pos + 1
    return render(request, 'conciertos/setlistentry_form.html', {'form': form, 'concert': concert, 'entry': entry, 'artists': artists, 'suggested_position': suggested_position})


@staff_member_required
@require_http_methods(['POST'])
def setlist_entry_delete(request, pk):
    """Staff-only deletion of a setlist entry (POST only)."""
    entry = get_object_or_404(SetlistEntry, pk=pk)
    concert_pk = entry.concert.pk
    entry.delete()
    return redirect('concert_setlist', pk=concert_pk)


@staff_member_required
@require_http_methods(['POST'])
def song_create_ajax(request):
    """AJAX endpoint to create a Song from the setlist form.

    Expects POST with 'title' (required), optional 'original_artist' and 'release_year'.
    Returns JSON with the created song id and title.
    """
    title = request.POST.get('title', '').strip()
    original_artist = request.POST.get('original_artist', '').strip()
    release_year = request.POST.get('release_year', '').strip()

    errors = {}
    if not title:
        errors['title'] = 'El título es obligatorio.'

    # Validate release_year if provided
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

    # Try to resolve original_artist to an Artist instance by exact name; if not found,
    # store the provided name in `original_artist_name` (we don't create new Artist rows).
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

