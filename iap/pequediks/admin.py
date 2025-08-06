from django.contrib import admin
from .models import coordinator, group, server, child, assistance, GroupCoordinator

@admin.register(coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    """
    Admin interface options for the coordinator model.
    """
    list_display = ('name', 'surname', 'user')
    search_fields = ('name', 'surname', 'user__username')
    # raw_id_fields es útil cuando tienes muchos usuarios para elegir.
    raw_id_fields = ('user',)

@admin.register(group)
class GroupAdmin(admin.ModelAdmin):
    """
    Admin interface options for the group model.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(server)
class ServerAdmin(admin.ModelAdmin):
    """
    Admin interface options for the server model.
    """
    list_display = ('name', 'surname', 'group', 'coordinator')
    search_fields = ('name', 'surname')
    list_filter = ('group', 'coordinator')
    autocomplete_fields = ['group', 'coordinator']

@admin.register(child)
class ChildAdmin(admin.ModelAdmin):
    """
    Admin interface options for the child model.
    """
    list_display = ('name', 'surname', 'birthday', 'calculated_age', 'status')
    search_fields = ('name', 'surname')
    list_filter = ('status',)
    # Hacemos que la edad calculada sea de solo lectura, ya que es una propiedad.
    readonly_fields = ('calculated_age',)

@admin.register(assistance)
class AssistanceAdmin(admin.ModelAdmin):
    """
    Admin interface options for the assistance model.
    """
    list_display = ('child', 'date', 'group', 'attended', 'coordinator')
    search_fields = ('child__name', 'child__surname')
    list_filter = ('date', 'group', 'attended')
    autocomplete_fields = ['child', 'group', 'coordinator']

@admin.register(GroupCoordinator)
class GroupCoordinatorAdmin(admin.ModelAdmin):
    """
    Admin interface options for the GroupCoordinator model.
    """
    list_display = ('group', 'coordinator')
    search_fields = ('group__name', 'coordinator__name', 'coordinator__surname')
    list_filter = ('group', 'coordinator')
    autocomplete_fields = ['group', 'coordinator']


