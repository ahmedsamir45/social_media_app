# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'bio', 'image', 'birth_date', 'exist_date')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
