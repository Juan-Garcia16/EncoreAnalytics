from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('artists/', views.ArtistListView.as_view(), name='artist_list'),
    path('artists/add/', views.ArtistCreateView.as_view(), name='artist_add'),
    # path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'), 
]