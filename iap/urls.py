from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

# --- Diagnóstico: Reactivación del Admin Site Aislado ---
# Se vuelve a habilitar el sitio de administración de depuración para poder
# gestionar usuarios y grupos mientras se investiga el conflicto en el sitio principal.
class MyAdminSite(admin.AdminSite):
    site_header = "IAP Admin de Depuración"

debug_admin_site = MyAdminSite(name='myadmin')
debug_admin_site.register(User)
debug_admin_site.register(Group)


@login_required
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls), # El sitio de admin original
    path('my-admin/', debug_admin_site.urls), # El sitio de admin de depuración
    path('academia/', include(('academia.urls', 'academia'), namespace='academia')), 
    path('alabanza/', include(('alabanza.urls', 'alabanza'), namespace='alabanza')),
    path('anfitriones/', include(('anfitriones.urls', 'anfitriones'), namespace='anfitriones')),
    path('cunakids/', include(('cunakids.urls', 'cunakids'), namespace='cunakids')),
    path('discipulado/', include(('discipulado.urls', 'discipulado'), namespace='discipulado')),
    path('encuentros/', include('encuentros.urls')),  # Si no usas namespace, puedes dejar así
    path('jap/', include('jap.urls')),
    path('jpro/', include('jpro.urls')),
    path('pusukids/', include(('pusukids.urls', 'pusukids'), namespace='pusukids')),    
    path('pequediks/', include(('pequediks.urls', 'pequediks'), namespace='pequediks')),
    path('account/', include('account.urls', namespace='account')),
    path('', home, name='home'),
]
