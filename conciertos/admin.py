from django.contrib import admin
from .models import Tour, Concert, Song, SetlistEntry

# Register your models here.
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('artist', 'name', 'start_date', 'end_date', 'status', 'total_income')
    search_fields = ('name', 'artist__name')
    
@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('artist', 'venue', 'tour', 'start_datetime', 'status', 'total_income')
    search_fields = ('artist__name', 'venue__name', 'tour__name')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_artist', 'release_year')
    search_fields = ('title', 'original_artist__name') 
    
@admin.register(SetlistEntry)
class SetlistEntryAdmin(admin.ModelAdmin):
    list_display = ('concert', 'song', 'position', 'section', 'is_cover')
    search_fields = ('concert__artist__name', 'song__title')
