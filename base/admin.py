from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PresidentClub

@admin.register(PresidentClub)
class PresidentClubAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "date_creation")
    search_fields = ("prenom", "nom")
    ordering = ("-date_creation",)