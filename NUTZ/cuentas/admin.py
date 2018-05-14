from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminActualizarForm, UserAdminCrearForm
from .models import User

class UserAdmin(BaseUserAdmin):
    # Los forms para añadir y cambiar isntancias de usuarios
    form = UserAdminActualizarForm
    add_form = UserAdminCrearForm
    
    list_display = ('email', 'rut','admin', 'es_paciente', 'es_nutri')
    list_filter = ('admin', 'es_paciente', 'es_nutri')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Información personal', {'fields': ('rut', 'nombres','apellidos', 'nacimiento', 'genero')}),
        ('Paciente', {'fields': ('es_paciente',)}),
        ('Nutricionista', {'fields': ('es_nutri',)}),
        ('Permisos', {'fields': ('admin','staff', 'active','es_superadmin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('rut','email', 'password1', 'password2','es_paciente', 'es_nutri', 'es_superadmin')}
        ),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


