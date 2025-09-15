from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConcertListView.as_view(), name='concert_list'),
    path('concerts/add/', views.ConcertCreateView.as_view(), name='concert_add'),
]