from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Tour, Concert, Song, SetlistEntry
from .forms import ConcertForm
from django.db.models import Q
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
                Q(artist__name__icontains=q) | Q(venue__name__icontains=q)
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
        return context

class ConcertCreateView(CreateView):
    model = Concert
    form_class = ConcertForm
    template_name = 'conciertos/concert_form.html'
    success_url = reverse_lazy('concert_list')

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

