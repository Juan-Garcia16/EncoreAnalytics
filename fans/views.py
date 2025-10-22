from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Fan, Attendance, Interest
from django.contrib.auth import login
from .forms import UserRegisterForm, FanProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
    
    
# ----- REGISTER FAN VIEW -----
def register(request):
    if request.method == 'POST':
        uform = UserRegisterForm(request.POST)
        pform = FanProfileForm(request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            user.email = uform.cleaned_data['email']
            user.save()
            # crear perfil fan
            profile = pform.save(commit=False)
            profile.user = user
            # si no provees email en profile, aseguramos que coincida
            if not profile.email:
                profile.email = user.email
            profile.save()
            login(request, user)  # loguea al usuario recién creado
            return redirect('home')
    else:
        uform = UserRegisterForm()
        pform = FanProfileForm()
    return render(request, 'users/register.html', {'uform': uform, 'pform': pform})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Django por defecto autentica por username, así que
        # si registras por email, debemos buscar el username.
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Cambia por la vista que usarás tras login
        else:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'users/login.html')
