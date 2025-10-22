from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('', views.FanListView.as_view(), name='fan_list'),
    path('add/', views.FanCreateView.as_view(), name='fan_add'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('interest/', views.InterestListView.as_view(), name='interest_list'),
    path('interest/add/', views.InterestCreateView.as_view(), name='interest_add'),
]