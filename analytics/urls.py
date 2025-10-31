from django.urls import path
from . import views

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
]
