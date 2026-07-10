from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Follow

class CustomUserAdmin(UserAdmin):
    # Campi custom per la modifica dell'utente
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('role', 'bio')}),
    )
    
    # Mostra il ruolo direttamente nella tabella riassuntiva degli utenti
    list_display = ['username', 'email', 'role', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)