from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'est_valide', 'est_actif')
    list_filter = ('user_type', 'est_valide', 'est_actif')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_type', 'telephone', 'adresse', 'photo',
                       'est_valide', 'technicien', 'commercial'),
        }),
    )


admin.site.register(User, CustomUserAdmin)