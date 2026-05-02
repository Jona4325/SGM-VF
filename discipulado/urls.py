from django.urls import path
from . import views

app_name = 'discipulado'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    path('', views.index, name='index'),

    path('disciples/', views.DiscipleListView.as_view(), name='disciple_list'),
    path('disciples/new/', views.DiscipleCreateView.as_view(), name='disciple_create'),
    path('disciples/<int:pk>/edit/', views.DiscipleUpdateView.as_view(), name='disciple_update'),
    path('disciples/<int:pk>/delete/', views.DiscipleDeleteView.as_view(), name='disciple_delete'),

    path('host-families/', views.HostFamilyListView.as_view(), name='host_family_list'),
    path('host-families/new/', views.HostFamilyCreateView.as_view(), name='host_family_create'),
    path('host-families/<int:pk>/edit/', views.HostFamilyUpdateView.as_view(), name='host_family_update'),
    path('host-families/<int:pk>/delete/', views.HostFamilyDeleteView.as_view(), name='host_family_delete'),

    path('supervisors/', views.SupervisorListView.as_view(), name='supervisor_list'),
    path('supervisors/new/', views.SupervisorCreateView.as_view(), name='supervisor_create'),
    path('supervisors/<int:pk>/edit/', views.SupervisorUpdateView.as_view(), name='supervisor_update'),
    path('supervisors/<int:pk>/delete/', views.SupervisorDeleteView.as_view(), name='supervisor_delete'),

    path('groups/', views.DiscipleshipGroupListView.as_view(), name='group_list'),
    path('groups/new/', views.DiscipleshipGroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', views.DiscipleshipGroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', views.DiscipleshipGroupDeleteView.as_view(), name='group_delete'),

    path('group-members/', views.DiscipleshipGroupMemberListView.as_view(), name='group_member_list'),
    path('group-members/new/', views.DiscipleshipGroupMemberCreateView.as_view(), name='group_member_create'),
    path('group-members/<int:pk>/edit/', views.DiscipleshipGroupMemberUpdateView.as_view(), name='group_member_update'),
    path('group-members/<int:pk>/delete/', views.DiscipleshipGroupMemberDeleteView.as_view(), name='group_member_delete'),

    path('meetings/', views.DiscipleshipMeetingListView.as_view(), name='meeting_list'),
    path('meetings/new/', views.DiscipleshipMeetingCreateView.as_view(), name='meeting_create'),
    path('meetings/<int:pk>/edit/', views.DiscipleshipMeetingUpdateView.as_view(), name='meeting_update'),
    path('meetings/<int:pk>/delete/', views.DiscipleshipMeetingDeleteView.as_view(), name='meeting_delete'),

    path('attendance/', views.MeetingAttendanceListView.as_view(), name='attendance_list'),
    path('attendance/meeting/<int:meeting_id>/batch/', views.batch_attendance_create, name='attendance_batch_create'),

    path('offerings/', views.OfferingIncomeListView.as_view(), name='offering_list'),
    path('offerings/new/', views.OfferingIncomeCreateView.as_view(), name='offering_create'),
    path('offerings/<int:pk>/edit/', views.OfferingIncomeUpdateView.as_view(), name='offering_update'),
    path('offerings/<int:pk>/delete/', views.OfferingIncomeDeleteView.as_view(), name='offering_delete'),

    path('expenses/', views.MeetingExpenseListView.as_view(), name='expense_list'),
    path('expenses/new/', views.MeetingExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/edit/', views.MeetingExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/<int:pk>/delete/', views.MeetingExpenseDeleteView.as_view(), name='expense_delete'),

    path('reports/', views.reports, name='reports'),
]