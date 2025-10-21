from django.urls import path
from . import views 

urlpatterns = [
    path('', views.FanListView.as_view(), name='fan_list'),
    path('add/', views.FanCreateView.as_view(), name='fan_add'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('interest/', views.InterestListView.as_view(), name='interest_list'),
    path('interest/add/', views.InterestCreateView.as_view(), name='interest_add'),
]