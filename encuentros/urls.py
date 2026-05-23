from django.urls import path
from . import views

app_name = 'encuentros'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    path('', views.index, name='index'),  # URL para la página principal de encuentros

    # URLs para Meeting
    path('meetings/', views.MeetingListView.as_view(), name='meeting-list'),
    path('meetings/new/', views.MeetingCreateView.as_view(), name='meeting-create'),
    path('meetings/<int:pk>/', views.MeetingDetailView.as_view(), name='meeting-detail'),
    path('meetings/<int:pk>/edit/', views.MeetingUpdateView.as_view(), name='meeting-update'),
    path('meetings/<int:pk>/delete/', views.MeetingDeleteView.as_view(), name='meeting-delete'),

    # URLs para Server
    path('servers/', views.ServerListView.as_view(), name='server-list'),
    path('servers/new/', views.ServerCreateView.as_view(), name='server-create'),
    path('servers/<int:pk>/', views.ServerDetailView.as_view(), name='server-detail'),
    path('servers/<int:pk>/edit/', views.ServerUpdateView.as_view(), name='server-update'),
    path('servers/<int:pk>/delete/', views.ServerDeleteView.as_view(), name='server-delete'),

    # URLs para Participant
    path('participants/', views.ParticipantListView.as_view(), name='participant-list'),
    path('participants/new/', views.ParticipantCreateView.as_view(), name='participant-create'),
    path('participants/<int:pk>/', views.ParticipantDetailView.as_view(), name='participant-detail'),
    path('participants/<int:pk>/edit/', views.ParticipantUpdateView.as_view(), name='participant-update'),
    path('participants/<int:pk>/delete/', views.ParticipantDeleteView.as_view(), name='participant-delete'),

    # URLs para FamilyParticipantInfo
    path('familyinfo/', views.FamilyParticipantInfoListView.as_view(), name='familyparticipantinfo-list'),
    path('familyinfo/new/', views.FamilyParticipantInfoCreateView.as_view(), name='familyparticipantinfo-create'),
    path('familyinfo/<int:pk>/', views.FamilyParticipantInfoDetailView.as_view(), name='familyparticipantinfo-detail'),
    path('familyinfo/<int:pk>/edit/', views.FamilyParticipantInfoUpdateView.as_view(), name='familyparticipantinfo-update'),
    path('familyinfo/<int:pk>/delete/', views.FamilyParticipantInfoDeleteView.as_view(), name='familyparticipantinfo-delete'),

    # URLs para ChurchDataInfo
    path('churchdata/', views.ChurchDataInfoListView.as_view(), name='churchdatainfo-list'),
    path('churchdata/new/', views.ChurchDataInfoCreateView.as_view(), name='churchdatainfo-create'),
    path('churchdata/<int:pk>/', views.ChurchDataInfoDetailView.as_view(), name='churchdatainfo-detail'),
    path('churchdata/<int:pk>/edit/', views.ChurchDataInfoUpdateView.as_view(), name='churchdatainfo-update'),
    path('churchdata/<int:pk>/delete/', views.ChurchDataInfoDeleteView.as_view(), name='churchdatainfo-delete'),

    # URLs para MeetingParticipant
    path('meetingattendance/', views.MeetingParticipantListView.as_view(), name='meetingparticipant-list'),
    path('meetingattendance/new/', views.MeetingParticipantCreateView.as_view(), name='meetingparticipant-create'),
    path('meetingattendance/<int:pk>/', views.MeetingParticipantDetailView.as_view(), name='meetingparticipant-detail'),
    path('meetingattendance/<int:pk>/edit/', views.MeetingParticipantUpdateView.as_view(), name='meetingparticipant-update'),
    path('meetingattendance/<int:pk>/delete/', views.MeetingParticipantDeleteView.as_view(), name='meetingparticipant-delete'),

    # URLs para FinanceMovements
    path('finance/', views.FinanceMovementsListView.as_view(), name='financemovements-list'),
    path('finance/new/', views.FinanceMovementsCreateView.as_view(), name='financemovements-create'),
    path('finance/<int:pk>/', views.FinanceMovementsDetailView.as_view(), name='financemovements-detail'),
    path('finance/<int:pk>/edit/', views.FinanceMovementsUpdateView.as_view(), name='financemovements-update'),
    path('finance/<int:pk>/delete/', views.FinanceMovementsDeleteView.as_view(), name='financemovements-delete'),

    # URLs para Summary
    path('summaries/', views.SummaryListView.as_view(), name='summary-list'),
    path('summaries/generate/', views.GenerateSummaryView.as_view(), name='summary-generate'),
    # La URL para generar para un meeting específico podría ser más RESTful, ej. /meetings/<int:meeting_pk>/summary/generate/
    path('summaries/<int:pk>/', views.SummaryDetailView.as_view(), name='summary-detail'),
    path('summaries/<int:pk>/delete/', views.SummaryDeleteView.as_view(), name='summary-delete'),
]