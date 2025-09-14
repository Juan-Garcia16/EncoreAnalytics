from django.contrib import admin
from .models import Fan, Attendance, Interest

# Register your models here.
@admin.register(Fan)
class FanAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'city', 'birthdate')
    search_fields = ('full_name', 'email')
    list_filter = ('city',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('fan', 'concert', 'rating')
    search_fields = ('fan__full_name', 'concert__artist__name', 'concert__venue__name')
    list_filter = ('concert',)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('fan', 'concert', 'created_at')
    search_fields = ('fan__full_name', 'concert__artist__name', 'concert__venue__name')
    list_filter = ('created_at',)