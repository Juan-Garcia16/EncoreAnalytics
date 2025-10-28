from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Fan
from core.models import City


class RegisterCreatesUserAndFanTest(TestCase):
	def test_register_creates_user_and_fan(self):
		# Crear una ciudad para el formulario (si se usa ModelChoiceField)
		city = City.objects.create(name='TestCity', country='TestCountry')

		register_url = reverse('register')
		data = {
			'username': 'tester',
			'email': 'tester@example.com',
			'password1': 'complexpassword123',
			'password2': 'complexpassword123',
			'full_name': 'Test User',
			'city': city.pk,
			'birthdate': '1990-01-01',
		}

		users_before = User.objects.count()
		fans_before = Fan.objects.count()

		resp = self.client.post(register_url, data, follow=True)

		self.assertEqual(User.objects.count(), users_before + 1)
		self.assertEqual(Fan.objects.count(), fans_before + 1)

		# Verificar que el fan esté vinculado al usuario creado
		user = User.objects.get(username='tester')
		fan = Fan.objects.get(email='tester@example.com')
		self.assertIsNotNone(fan)
		# Si existe el atributo user en Fan (OneToOne) debe apuntar al user
		self.assertEqual(fan.user, user)
