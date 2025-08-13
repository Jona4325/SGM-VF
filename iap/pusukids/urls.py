from django.urls import path
from . import views

app_name = 'pusukids'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    path('', views.index, name='index'),  # URL para la página principal de pusukids

    # URLs para el CRUD de Coordinator
    path('coordinators/', views.coordinator_list, name='coordinator_list'),
    path('coordinators/new/', views.coordinator_create, name='coordinator_create'),
    path('coordinators/<int:pk>/edit/', views.coordinator_update, name='coordinator_update'),
    path('coordinators/<int:pk>/delete/', views.coordinator_delete, name='coordinator_delete'),

    #urls para el CRUD de Group
    path('groups/', views.group_list, name='group_list'),
    path('groups/new/', views.group_create, name='group_create'),
    path('groups/<int:pk>/edit/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),

    # --- URLs para Server ---
    path('servers/', views.ServerListView.as_view(), name='server_list'),
    path('servers/<int:pk>/', views.ServerDetailView.as_view(), name='server_detail'),
    path('servers/new/', views.ServerCreateView.as_view(), name='server_create'),
    path('servers/<int:pk>/edit/', views.ServerUpdateView.as_view(), name='server_update'),
    path('servers/<int:pk>/delete/', views.ServerDeleteView.as_view(), name='server_delete'),

    # Rutas para groupage
    path('groupages/', views.groupage_list, name='groupage_list'),
    path('groupages/create/', views.groupage_create, name='groupage_create'),
    path('groupages/<int:pk>/update/', views.groupage_update, name='groupage_update'),
    path('groupages/<int:pk>/delete/', views.groupage_delete, name='groupage_delete'),

    # --- URLs para Child --- (Actualizadas)
    path('children/', views.child_list, name='child_list'), # <-- Cambiado
    path('children/new/', views.child_create, name='child_create'), # <-- Cambiado
    path('children/<int:pk>/edit/', views.child_update, name='child_update'), # <-- Cambiado
    path('children/<int:pk>/delete/', views.child_delete, name='child_delete'), # <-- Cambiado

    # --- URLs para Assistance --- NUEVAS RUTAS ---
    path('assistances/', views.assistance_list, name='assistance_list'),
    path('assistances/new/', views.assistance_create, name='assistance_create'),
    path('assistances/<int:pk>/edit/', views.assistance_update, name='assistance_update'),
    path('assistances/<int:pk>/delete/', views.assistance_delete, name='assistance_delete'),

    # --- URLs para Weekinfo ---
    path('weekinfos/', views.weekinfo_list, name='weekinfo_list'),
    path('weekinfos/new/', views.weekinfo_create, name='weekinfo_create'),
    path('weekinfos/<int:pk>/edit/', views.weekinfo_update, name='weekinfo_update'),
    path('weekinfos/<int:pk>/delete/', views.weekinfo_delete, name='weekinfo_delete'),

    # --- URLs para Expense ---
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/new/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # --- URLs para Fecha ---
    path('fechas/', views.fecha_list, name='fecha_list'),
    path('fechas/new/', views.fecha_create, name='fecha_create'),
    path('fechas/<int:pk>/edit/', views.fecha_update, name='fecha_update'),
    path('fechas/<int:pk>/delete/', views.fecha_delete, name='fecha_delete'),

    # --- URLs para GroupCoordinator ---
    path('groupcoordinators/', views.groupcoordinator_list, name='groupcoordinator_list'),
    path('groupcoordinators/new/', views.groupcoordinator_create, name='groupcoordinator_create'),
    path('groupcoordinators/<int:pk>/edit/', views.groupcoordinator_update, name='groupcoordinator_update'),
    path('groupcoordinators/<int:pk>/delete/', views.groupcoordinator_delete, name='groupcoordinator_delete'),
]