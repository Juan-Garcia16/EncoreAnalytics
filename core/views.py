from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Artist, City, Venue

# Create your views here.
def HomeView(request):
    return render(request, 'home.html')

# Artist views
class ArtistListView(ListView):
    model = Artist
    template_name = 'core/artist_list.html'
    context_object_name = 'artists'
    queryset = Artist.objects.all().order_by('name')

class ArtistCreateView(CreateView):
    model = Artist
    template_name = 'core/artist_form.html'
    fields = ['name', 'country', 'debut_year', 'genre']
    success_url = reverse_lazy('artist_list')
    
# City views
class CityListView(ListView):
    model = City
    template_name = 'core/city_list.html'
    context_object_name = 'cities'
    queryset = City.objects.all().order_by('name')

class CityCreateView(CreateView):
    model = City
    template_name = 'core/city_form.html'
    fields = ['name', 'country']
    success_url = reverse_lazy('city_list')
    
# Venue views
class VenueListView(ListView):
    model = Venue
    template_name = 'core/venue_list.html'
    context_object_name = 'venues'
    queryset = Venue.objects.select_related('city').all().order_by('name')

class VenueCreateView(CreateView):
    model = Venue
    template_name = 'core/venue_form.html'
    fields = ['name', 'address', 'capacity', 'city']
    success_url = reverse_lazy('venue_list')