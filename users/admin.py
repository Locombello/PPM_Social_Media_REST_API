from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Aggiungiamo i nostri campi custom alla pagina di modifica dell'utente
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('role', 'bio')}),
    )
    
    # Opzionale: mostriamo il ruolo direttamente nella tabella riassuntiva degli utenti
    list_display = ['username', 'email', 'role', 'is_staff']

# Sostituiamo la registrazione di default con la nostra classe personalizzata
admin.site.register(CustomUser, CustomUserAdmin)