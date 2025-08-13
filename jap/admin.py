from django.contrib import admin
from .models import coordinator, group, server, child, assistance, GroupCoordinator

# Register your models here.

@admin.register(coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    """
    Admin view for Coordinator model.
    """
    list_display = ('name', 'surname', 'user')
    search_fields = ('name', 'surname', 'user__username')
    list_select_related = ('user',)

@admin.register(group)
class GroupAdmin(admin.ModelAdmin):
    """
    Admin view for Group model.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(server)
class ServerAdmin(admin.ModelAdmin):
    """
    Admin view for Server model.
    """
    list_display = ('name', 'surname', 'coordinator', 'group')
    list_filter = ('group', 'coordinator')
    search_fields = ('name', 'surname', 'coordinator__name', 'group__name')
    list_select_related = ('coordinator', 'group')

@admin.register(child)
class ChildAdmin(admin.ModelAdmin):
    """
    Admin view for Child model.
    """
    list_display = ('name', 'surname', 'birthday', 'calculated_age', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'surname', 'parent_name')
    readonly_fields = ('calculated_age',)

@admin.register(assistance)
class AssistanceAdmin(admin.ModelAdmin):
    list_display = ('child', 'date', 'group', 'coordinator', 'attended')
    list_filter = ('date', 'attended', 'group', 'coordinator')
    search_fields = ('child__name', 'child__surname')
    list_select_related = ('child', 'group', 'coordinator')

@admin.register(GroupCoordinator)
class GroupCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('group', 'coordinator')
    list_filter = ('group', 'coordinator')
    search_fields = ('group__name', 'coordinator__name', 'coordinator__surname')
    list_select_related = ('group', 'coordinator')

