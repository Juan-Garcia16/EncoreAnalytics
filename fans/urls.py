from django.urls import path
from . import views 

urlpatterns = [
    path('', views.FanListView.as_view(), name='fan_list'),
    path('add/', views.FanCreateView.as_view(), name='fan_add'),
]