from django.urls import path
from . import views

app_name = 'anfitriones'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    path('', views.index, name='index'),  # URL para la página principal de academia
    
    # URLs para Coordinator CRUD
    path('coordinators/', views.CoordinatorListView.as_view(), name='coordinator_list'),
    path('coordinators/new/', views.CoordinatorCreateView.as_view(), name='coordinator_create'),
    path('coordinators/<int:pk>/edit/', views.CoordinatorUpdateView.as_view(), name='coordinator_update'),
    path('coordinators/<int:pk>/delete/', views.CoordinatorDeleteView.as_view(), name='coordinator_delete'),
       # URLs para Group CRUD
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/new/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
        # URLs para Server CRUD
    path('servers/', views.ServerListView.as_view(), name='server_list'),
    path('servers/new/', views.ServerCreateView.as_view(), name='server_create'),
    path('servers/<int:pk>/edit/', views.ServerUpdateView.as_view(), name='server_update'),
    path('servers/<int:pk>/delete/', views.ServerDeleteView.as_view(), name='server_delete'),
    # URLs para Ministry CRUD
    path('ministries/', views.MinistryListView.as_view(), name='ministry_list'),
    path('ministries/new/', views.MinistryCreateView.as_view(), name='ministry_create'),
    path('ministries/<int:pk>/edit/', views.MinistryUpdateView.as_view(), name='ministry_update'),
    path('ministries/<int:pk>/delete/', views.MinistryDeleteView.as_view(), name='ministry_delete'),
    # URLs para Assistance CRUD
    path('assistances/', views.AssistanceListView.as_view(), name='assistance_list'),
    # path('assistances/new/', views.AssistanceCreateView.as_view(), name='assistance_create'), # Comentado para reemplazar por el lote
    path('assistances/batch/', views.batch_assistance_create, name='assistance_batch_create'),
    path('assistances/<int:pk>/edit/', views.AssistanceUpdateView.as_view(), name='assistance_update'),
    path('assistances/<int:pk>/delete/', views.AssistanceDeleteView.as_view(), name='assistance_delete'),
    # URLs para Attendance CRUD (Estadísticas de Grupo)
    path('attendances/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendances/new/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendances/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendances/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),
    path('summary/', views.summary, name='summary'),
]