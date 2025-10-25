from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Artist, City, Venue
from .forms import ArtistForm
from .countries import get_countries
from .genres import get_genres
from django.db.models import Q

# Create your views here.
def HomeView(request):
    return render(request, 'base.html')

# Artist views
class ArtistListView(ListView):
    model = Artist
    template_name = 'core/artist_list.html'
    context_object_name = 'artists'
    queryset = Artist.objects.all().order_by('name')

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('query_artists', '').strip()
        if q:
            # Buscar por nombre, país o género (case-insensitive)
            qs = qs.filter(
                Q(name__icontains=q) | Q(country__icontains=q) | Q(genre__icontains=q)
            ).order_by('name')
        return qs

class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'core/artist_form.html'
    success_url = reverse_lazy('artist_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # lista de países para el datalist en el formulario
        context['countries'] = get_countries()
        # lista de géneros para el datalist en el formulario
        context['genres'] = get_genres()
        return context


class ArtistUpdateView(UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'core/artist_form.html'
    success_url = reverse_lazy('artist_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = get_countries()
        context['genres'] = get_genres()
        return context
    
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