from .models import Adoption, Contact, CustomUser, lostandfound, Breed
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'country','city', 'contact', 'age'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'country', 'city', 'contact', 'age')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),

    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'country', 'city', 'contact', 'age')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),

    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Adoption)
admin.site.register(lostandfound)
admin.site.register(Contact)
admin.site.register(Breed)