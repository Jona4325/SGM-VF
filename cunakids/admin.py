# c:\Proyectos\pusuqui1\iap\cunakids\admin.py

from django.contrib import admin
# Importa todos tus modelos
from .models import (
    coordinator,
    group,
    server,
    child,
    assistance, GroupCoordinator,

)
# Importa date de datetime
from datetime import date # <--- Asegúrate que esta línea existe

# --- Clases de Administración Personalizadas (ModelAdmin) ---

@admin.register(coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'user')
    search_fields = ('name', 'surname', 'user__username')
    # raw_id_fields facilita la selección de usuarios cuando hay muchos
    raw_id_fields = ('user',)

@admin.register(group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'coordinator', 'group')
    list_filter = ('coordinator', 'group')
    search_fields = ('name', 'surname')
    raw_id_fields = ('coordinator', 'group')

@admin.register(child)
class ChildAdmin(admin.ModelAdmin):
    # Configuración mínima para probar la carga de la lista
    list_display = ('name', 'surname', 'birthday', 'status')
    search_fields = ('name', 'surname')
    list_filter = ('status',)

@admin.register(assistance)
class AssistanceAdmin(admin.ModelAdmin):
    list_display = ('child', 'date', 'group', 'coordinator', 'attended') # <-- Cambiado kid a child
    list_filter = ('date', 'group', 'coordinator', 'attended')
    search_fields = ('child__name', 'child__surname') # <-- Cambiado kid__ a child__
    raw_id_fields = ('child', 'group', 'coordinator') # <-- 'date' eliminado
    list_editable = ('attended',)

@admin.register(GroupCoordinator)
class GroupCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('group', 'coordinator')
    list_filter = ('group', 'coordinator')
    search_fields = ('group__name', 'coordinator__name', 'coordinator__surname')
    raw_id_fields = ('group', 'coordinator')
