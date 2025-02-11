from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'activo', 'fecha_inscripcion')
    list_filter = ('activo', 'fecha_inscripcion', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-fecha_inscripcion',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': (
            'first_name',
            'last_name',
            'email',
            'fecha_nacimiento',
            'telefono',
            'direccion',
        )}),
        ('Estado', {'fields': (
            'activo',
            'fecha_inscripcion',
        )}),
        ('Permisos', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('fecha_inscripcion',)