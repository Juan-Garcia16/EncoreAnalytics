from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Artist, City, Venue
from .forms import ArtistForm
from .countries import get_countries
from .genres import get_genres
from django.db.models import Q
from django.utils import timezone
from conciertos.models import Concert
from fans.models import Fan

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


def artist_delete(request, pk):
    """Delete an artist. Accepts POST only and redirects to artist list."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    artist = get_object_or_404(Artist, pk=pk)
    # Optional: restrict deletion to staff users
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('artist_list')
    artist.delete()
    return redirect('artist_list')


def dashboard(request):
    """Render the dashboard with simple metrics and upcoming concerts."""
    # conteos básicos
    artists_count = Artist.objects.count()
    concerts_count = Concert.objects.count()
    fans_count = Fan.objects.count()

    # próximos conciertos: programados y con fecha >= ahora
    now = timezone.now()
    upcoming_concerts = (
        Concert.objects.filter(status='scheduled', start_datetime__gte=now)
        .select_related('artist', 'venue')
        .order_by('start_datetime')[:6]
    )

    context = {
        'artists_count': artists_count,
        'concerts_count': concerts_count,
        'fans_count': fans_count,
        'upcoming_concerts': upcoming_concerts,
    }
    return render(request, 'dashboard.html', context)
    
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