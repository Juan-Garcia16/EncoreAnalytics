from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('artists/', views.ArtistListView.as_view(), name='artist_list'),
    path('artists/add/', views.ArtistCreateView.as_view(), name='artist_add'),
    path('artists/<int:pk>/edit/', views.ArtistUpdateView.as_view(), name='artist_edit'),
    path('artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
    path('cities/', views.CityListView.as_view(), name='city_list'),
    path('cities/add/', views.CityCreateView.as_view(), name='city_add'),   
    path('venues/', views.VenueListView.as_view(), name='venue_list'),
    path('venues/add/', views.VenueCreateView.as_view(), name='venue_add'),
    # path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'), 
]