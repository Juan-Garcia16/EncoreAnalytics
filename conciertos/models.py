from django.db import models
from core.models import Artist, Venue

# Create your models here.
class Tour(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tours') # relación con el artista (si se elimina el artista, se eliminan sus giras), un artista puede tener varias giras.
    name = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('planned','Planned'),('ongoing','Ongoing'),('finished','Finished')], default='planned')
    total_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.artist.name}"
    
class Concert(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='concerts')
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='concerts')
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True, blank=True, related_name='concerts') # gira asociada (puede estar vacío, si se elimina la gira, el campo queda nulo).
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('scheduled','Programado'),('completed','Realizado'),('canceled','Cancelado')], default='scheduled')
    total_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    img = models.URLField(null=True, blank=True)  # URL de la imagen promocional del concierto
    
    def __str__(self):
        return f"{self.artist.name} @ {self.venue.name} - {self.start_datetime.date()}"
    
class Song(models.Model):
    title = models.CharField(max_length=300)
    original_artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True)
    release_year = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class SetlistEntry(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='setlist_entries')
    song = models.ForeignKey(Song, on_delete=models.PROTECT)
    position = models.PositiveIntegerField()
    section = models.CharField(max_length=50, blank=True) 
    is_cover = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('concert', 'position') #asegura que no haya dos canciones en la misma posicion en un concierto
        ordering = ['position']
        
    def __str__(self):
        return f"{self.position} - {self.song.title})"