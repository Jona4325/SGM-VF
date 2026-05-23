from django.contrib import admin

from .models import (
	Disciple,
	DiscipleshipGroup,
	DiscipleshipGroupMember,
	DiscipleshipMeeting,
	HostFamily,
	MeetingAttendance,
	MeetingExpense,
	OfferingIncome,
	Supervisor,
	SupervisionVisit,
)


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'phone_number', 'status')
	search_fields = ('first_name', 'last_name', 'email', 'phone_number')
	list_filter = ('status',)


@admin.register(HostFamily)
class HostFamilyAdmin(admin.ModelAdmin):
	list_display = ('family_name', 'contact_name', 'contact_phone', 'status')
	search_fields = ('family_name', 'contact_name', 'contact_phone')
	list_filter = ('status',)


@admin.register(Disciple)
class DiscipleAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'phone_number', 'status')
	search_fields = ('first_name', 'last_name', 'email', 'phone_number')
	list_filter = ('status',)


class DiscipleshipGroupMemberInline(admin.TabularInline):
	model = DiscipleshipGroupMember
	extra = 1


@admin.register(DiscipleshipGroup)
class DiscipleshipGroupAdmin(admin.ModelAdmin):
	list_display = ('name', 'leader', 'coleader', 'host_family', 'supervisor', 'is_active')
	search_fields = ('name', 'leader__first_name', 'leader__last_name')
	list_filter = ('is_active',)
	inlines = [DiscipleshipGroupMemberInline]


@admin.register(DiscipleshipMeeting)
class DiscipleshipMeetingAdmin(admin.ModelAdmin):
	list_display = ('group', 'meeting_date', 'status', 'total_offerings', 'total_expenses', 'balance')
	search_fields = ('group__name', 'topic')
	list_filter = ('status', 'meeting_date')


@admin.register(MeetingAttendance)
class MeetingAttendanceAdmin(admin.ModelAdmin):
	list_display = ('meeting', 'disciple', 'status')
	search_fields = ('meeting__group__name', 'disciple__first_name', 'disciple__last_name')
	list_filter = ('status', 'meeting__meeting_date')


@admin.register(OfferingIncome)
class OfferingIncomeAdmin(admin.ModelAdmin):
	list_display = ('meeting', 'amount', 'category', 'received_from', 'registered_at')
	search_fields = ('meeting__group__name', 'notes')
	list_filter = ('category', 'registered_at')


@admin.register(MeetingExpense)
class MeetingExpenseAdmin(admin.ModelAdmin):
	list_display = ('meeting', 'amount', 'category', 'description', 'registered_at')
	search_fields = ('meeting__group__name', 'description', 'paid_to')
	list_filter = ('category', 'registered_at')


@admin.register(SupervisionVisit)
class SupervisionVisitAdmin(admin.ModelAdmin):
	list_display = ('supervisor', 'meeting', 'visit_date')
	search_fields = ('supervisor__first_name', 'supervisor__last_name', 'meeting__group__name')
	list_filter = ('visit_date',)
