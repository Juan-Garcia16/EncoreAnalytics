from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Fan
from core.models import City

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
            'placeholder': 'Tu nombre de usuario'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
            'placeholder': 'tu@correo.com'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
            'placeholder': 'Crea una contraseña'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
            'placeholder': 'Crea una contraseña'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class FanProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
            'placeholder': 'Tu nombre completo'
        })
    )
    
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input h-14 w-full flex-1 rounded-lg border-none bg-[#232f48] p-4 text-base text-white placeholder:text-[#92a4c9] focus:ring-2 focus:ring-primary',
            'placeholder': 'Tu ciudad'
        })
    )

    # Reemplazamos el campo de texto por un ModelChoiceField en la inicialización
    # para aprovechar la relación FK a City y evitar errores de tipo.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # si hay ciudades en la base, mostrar como select; si no, fall back a text input
        cities = City.objects.all()
        if cities.exists():
            self.fields['city'] = forms.ModelChoiceField(
                queryset=cities,
                required=False,
                widget=forms.Select(attrs={
                    'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal'
                })
            )
        else:
            # dejar el campo de texto si no hay ciudades cargadas
            self.fields['city'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
                    'placeholder': 'Tu ciudad'
                })
            )
    
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-gray-700 bg-[#1f1f1f] focus:border-primary h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal',
            'placeholder': 'YYYY-MM-DD',
            'type': 'date'
        })
    )
    
    class Meta:
        model = Fan
        # No incluir 'email' aquí: lo gestionamos en el User (UserRegisterForm).
        fields = ("full_name", "city", "birthdate")
