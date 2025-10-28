from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Fan, Attendance, Interest
from django.contrib.auth import login
from .forms import UserRegisterForm, FanProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.db import transaction
from django import forms
from core.models import City
# Create your views here.

# ----- FAN -----
class FanListView(ListView):
    model = Fan
    template_name = 'fans/fan_list.html'
    context_object_name = 'fans'
    qeryset = Fan.objects.all().order_by('full_name')
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('query_fans', '').strip()
        if q:
            # Buscar por nombre o ciudad (case-insensitive)
            qs = qs.filter(
                Q(full_name__icontains=q) | Q(city__name__icontains=q)
            ).order_by('full_name')
        return qs

class FanCreateView(CreateView):
    model = Fan
    form_class = FanProfileForm
    template_name = 'fans/fan_form.html'
    success_url = reverse_lazy('fan_list')
    
    #SE PODRIA AÑADIR LISTA DE CIUDADES PARA EL FORMULARIO

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
            # Crear usuario y perfil en una transacción atómica
            with transaction.atomic():
                user = uform.save(commit=False)
                user.email = uform.cleaned_data.get('email')
                user.save()

                # crear perfil fan (no commit todavía)
                profile = pform.save(commit=False)
                # vincular user con fan
                profile.user = user
                # si no provees email en profile, aseguramos que coincida
                if not profile.email:
                    profile.email = user.email

                # Manejar city: si el formulario devolvió un objeto City, asignarlo.
                cd_city = pform.cleaned_data.get('city')
                if isinstance(cd_city, City):
                    profile.city = cd_city
                else:
                    # si se recibió un string (fallback), intentar obtener o crear la ciudad
                    if isinstance(cd_city, str) and cd_city.strip():
                        city_obj, _ = City.objects.get_or_create(name=cd_city.strip(), defaults={'country': ''})
                        profile.city = city_obj

                profile.save()
            # loguear al usuario recién creado
            login(request, user)
            return redirect('home')
        else:
            # Registrar los errores para visibilidad: añadir mensajes y print a consola
            # (esto ayuda a debuggear cuando la página simplemente se recarga)
            for field, errs in uform.errors.items():
                for e in errs:
                    messages.error(request, f"User form - {field}: {e}")
            for field, errs in pform.errors.items():
                for e in errs:
                    messages.error(request, f"Profile form - {field}: {e}")
            # también volcar al stdout para quien corra el servidor
            print('REGISTER — user form errors:', uform.errors.as_json())
            print('REGISTER — profile form errors:', pform.errors.as_json())
    else:
        uform = UserRegisterForm()
        pform = FanProfileForm()
    return render(request, 'users/register.html', {'uform': uform, 'pform': pform})

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')  # puede ser correo o username
        password = request.POST.get('password')

        from django.contrib.auth.models import User
        user = None

        # Intentar autenticar directamente usando lo ingresado como username
        if identifier and password:
            user = authenticate(request, username=identifier, password=password)

        # Si no se autenticó, intentar tratar el identificador como email
        if user is None and identifier and password:
            # buscar usuarios con ese email (case-insensitive). Puede haber múltiples; probamos hasta autenticar.
            users_by_email = User.objects.filter(email__iexact=identifier)
            for u in users_by_email:
                user = authenticate(request, username=u.username, password=password)
                if user:
                    break

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Cambia por la vista que usarás tras login
        else:
            messages.error(request, 'Usuario/correo o contraseña incorrectos')

    return render(request, 'users/login.html')
