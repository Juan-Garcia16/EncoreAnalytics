from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    # Usamos la vista personalizada `login_view` para permitir login por correo
    path('login/', views.login_view, name='login'),
    # Forzar redirect al login después de logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('', views.FanListView.as_view(), name='fan_list'),
    path('add/', views.FanCreateView.as_view(), name='fan_add'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('interest/', views.InterestListView.as_view(), name='interest_list'),
    path('interest/add/', views.InterestCreateView.as_view(), name='interest_add'),
    # AJAX endpoints for toggling interest and getting counts
    path('concert/<int:concert_id>/toggle_interest/', views.toggle_interest, name='toggle_interest'),
    path('concert/<int:concert_id>/interest_count/', views.interest_count, name='interest_count'),
    path('concert/<int:concert_id>/rate/', views.rate_concert, name='rate_concert'),
]