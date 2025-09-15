from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConcertListView.as_view(), name='concierto_list'),
    path('add/', views.ConcertCreateView.as_view(), name='concierto_add'),
]