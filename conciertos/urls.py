from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConcertListView.as_view(), name='concert_list'),
    path('add/', views.ConcertCreateView.as_view(), name='concert_add'),
    path('<int:pk>/edit/', views.ConcertUpdateView.as_view(), name='concert_edit'),
    path('<int:pk>/delete/', views.concert_delete, name='concert_delete'),
]