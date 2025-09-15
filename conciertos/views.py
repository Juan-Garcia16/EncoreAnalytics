from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Tour, Concert, Song, SetlistEntry
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

class ConcertCreateView(CreateView):
    model = Concert
    fields = ['artist', 'venue', 'tour', 'start_datetime', 'status', 'total_income']
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

