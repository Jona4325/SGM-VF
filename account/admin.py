from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

# Define un nuevo User admin que extiende el de por defecto
class UserAdmin(BaseUserAdmin):
    # Aquí puedes añadir futuras personalizaciones al admin de usuarios
    pass

# Define un nuevo Group admin que extiende el de por defecto
class GroupAdmin(BaseGroupAdmin):
    # Aquí puedes añadir futuras personalizaciones al admin de grupos
    pass

# Desregistra los modelos base para evitar conflictos
admin.site.unregister(User)
admin.site.unregister(Group)

# Registra tus modelos con las nuevas clases de admin
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)