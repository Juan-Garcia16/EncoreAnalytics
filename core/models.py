from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    
    def __str__(self):
        return f"{self.name}, {self.country}"

class Artist(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=120)
    debut_year = models.PositiveSmallIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name
    
class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='venues') #relaciona el venue con la ciudad, si se borra la ciudad no se borran los venues asociados
    
    class Meta:
        unique_together = ('name', 'city') #asegura que no haya dos venues con el mismo nombre en la misma ciudad

    def __str__(self):
        return f"{self.name} ({self.city.name})"