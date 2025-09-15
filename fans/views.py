from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Fan, Attendance, Interest
# Create your views here.

# ----- FAN -----
class FanListView(ListView):
    model = Fan
    template_name = 'fans/fan_list.html'
    context_object_name = 'fans'

class FanCreateView(CreateView):
    model = Fan
    fields = ['full_name', 'email', 'city', 'birthdate'] #no se incluyeron favorite_concerts
    template_name = 'fans/fan_form.html'
    success_url = reverse_lazy('fan_list')

# ----- ATTENDANCE -----
class AttendanceListView(ListView):
    model = Attendance
    template_name = 'fans/attendance_list.html'
    context_object_name = 'attendances'

class AttendanceCreateView(CreateView):
    model = Attendance
    fields = ['fan', 'concert', 'rating']
    template_name = 'fans/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

# ----- INTEREST -----
class InterestListView(ListView):
    model = Interest
    template_name = 'fans/interest_list.html'
    context_object_name = 'interests'

class InterestCreateView(CreateView):
    model = Interest
    fields = ['fan', 'concert', 'created_at']
    template_name = 'fans/interest_form.html'
    success_url = reverse_lazy('interest_list')
