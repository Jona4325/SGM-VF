from django.urls import path
from . import views

app_name = 'alabanza'  # Namespace para las URLs de esta aplicación

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

    # URLs para Assistance
    path('assistance/', views.AssistanceListView.as_view(), name='assistance_list'),
    path('assistance/new/', views.AssistanceCreateView.as_view(), name='assistance_create'),
    path('assistance/<int:pk>/edit/', views.AssistanceUpdateView.as_view(), name='assistance_update'),
    path('assistance/<int:pk>/delete/', views.AssistanceDeleteView.as_view(), name='assistance_delete'),   

]
