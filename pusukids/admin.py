# c:\Proyectos\pusuqui1\iap\pusukids\admin.py

from django.contrib import admin
# Importa todos tus modelos
from .models import (
    coordinator,
    group,
    server,
    groupage,
    child, GroupCoordinator,
    fecha,
    assistance,
    weekinfo,
    expense,
)
# Importa date de datetime
from datetime import date # <--- Asegúrate que esta línea existe

# --- Clases de Administración Personalizadas (ModelAdmin) ---

@admin.register(coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
    search_fields = ('name', 'surname')

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

@admin.register(groupage)
class GroupageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(child)
class ChildAdmin(admin.ModelAdmin):
    # Configuración mínima para probar la carga de la lista
    list_display = ('name', 'surname', 'birthday', 'groupage', 'status')
    search_fields = ('name', 'surname')
    list_filter = ('groupage', 'status')
    list_editable = ('status',)

@admin.register(fecha)
class FechaAdmin(admin.ModelAdmin):
    list_display = ('date', 'week_no')
    list_filter = ('date',)
    ordering = ('-date',)

@admin.register(assistance)
class AssistanceAdmin(admin.ModelAdmin):
    list_display = ('child', 'date', 'group', 'coordinator', 'attended') # <-- Cambiado kid a child
    list_filter = ('date', 'group', 'coordinator', 'attended')
    search_fields = ('child__name', 'child__surname') # <-- Cambiado kid__ a child__
    raw_id_fields = ('child', 'date', 'group', 'coordinator') # <-- Cambiado kid a child
    list_editable = ('attended',)

@admin.register(weekinfo)
class WeekinfoAdmin(admin.ModelAdmin):
    # Asumiendo que los campos son IntegerField y FloatField como se discutió
    list_display = ('fecha', 'group', 'coordinator', 'total_kids_display', 'total_servers', 'money_collected')
    list_filter = ('fecha', 'group', 'coordinator')
    raw_id_fields = ('fecha', 'group', 'coordinator')

    # Si total_kids es IntegerField, puedes mostrarlo directamente o así:
    def total_kids_display(self, obj):
        return obj.total_kids # O cualquier formato que necesites
    total_kids_display.short_description = 'Total Niños' # Cambia el título de la columna

    # Nota: Asegúrate de que los campos en models.py para weekinfo sean correctos:
    # total_kids = models.IntegerField() # No ImageField
    # total_servers = models.IntegerField() # No el tipo IntegerField
    # money_collected = models.FloatField() # No el tipo FloatField

@admin.register(expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'fecha', 'reference')
    list_filter = ('fecha',)
    search_fields = ('description', 'reference')
    raw_id_fields = ('fecha',)

@admin.register(GroupCoordinator)
class GroupCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('group', 'coordinator')
    list_filter = ('group', 'coordinator')
    search_fields = ('group__name', 'coordinator__name', 'coordinator__surname')
    raw_id_fields = ('group', 'coordinator')
