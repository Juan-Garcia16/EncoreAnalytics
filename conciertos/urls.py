from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConcertListView.as_view(), name='concert_list'),
    path('add/', views.ConcertCreateView.as_view(), name='concert_add'),
    path('<int:pk>/edit/', views.ConcertUpdateView.as_view(), name='concert_edit'),
    path('<int:pk>/delete/', views.concert_delete, name='concert_delete'),
    path('<int:pk>/setlist/', views.concert_setlist, name='concert_setlist'),
    path('<int:concert_pk>/setlist/add/', views.setlist_entry_add, name='setlistentry_add'),
    path('setlist/song/add/', views.song_create_ajax, name='song_create_ajax'),
    path('setlist/<int:pk>/edit/', views.setlist_entry_edit, name='setlistentry_edit'),
    path('setlist/<int:pk>/delete/', views.setlist_entry_delete, name='setlistentry_delete'),
]