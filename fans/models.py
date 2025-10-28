from django.db import models
from django.conf import settings
from core.models import City
from conciertos.models import Concert
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Fan(models.Model):
    # Vinculación opcional con el usuario de Django.
    # Se deja null=True/blank=True para conservar compatibilidad con fans
    # creados antes de añadir usuarios.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='fan'
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    favorite_concerts = models.ManyToManyField(Concert, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.full_name

class Attendance(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, related_name='attendances')
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='attendees')
    rating = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    class Meta:
        unique_together = ('fan', 'concert')
    
class Interest(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, related_name='interests')
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='interested')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('fan', 'concert')
