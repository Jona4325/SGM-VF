from account.models import TenantMembership


def user_app_permissions(request):
    """
    Un procesador de contexto para añadir indicadores de acceso a las aplicaciones
    basándose en la pertenencia a grupos de Django.
    """
    user = request.user
    if not user.is_authenticated:
        return {}

    # Diccionario para los indicadores de acceso, por defecto en falso.
    app_perms = {
        'can_access_cunakids': False,
        'can_access_academia': False,
        'can_access_alabanza': False,
        'can_access_anfitriones': False,
        'can_access_discipulado': False,
        'can_access_encuentros': False,
        'can_access_jap': False,
        'can_access_multimedia': False,
        'can_access_pusukids': False,
        'can_access_pequediks': False,
        'can_access_jpro': False,
    }

    # Los superusuarios siempre tienen acceso a todo.
    if user.is_superuser:
        for key in app_perms:
            app_perms[key] = True
    else:
        group_names = set(user.groups.values_list('name', flat=True))

        if 'cunakids_staff' in group_names:
            app_perms['can_access_cunakids'] = True
        if 'Maestros' in group_names:
            app_perms['can_access_academia'] = True
        if 'alabanza_staff' in group_names:
            app_perms['can_access_alabanza'] = True
        if 'anfitriones_staff' in group_names:
            app_perms['can_access_anfitriones'] = True
        if 'discipulado_staff' in group_names:
            app_perms['can_access_discipulado'] = True
        if 'encuentros_staff' in group_names:
            app_perms['can_access_encuentros'] = True
        if 'jap_staff' in group_names:
            app_perms['can_access_jap'] = True
        if 'pusukids_staff' in group_names:
            app_perms['can_access_pusukids'] = True
        if 'pequediks_staff' in group_names:
            app_perms['can_access_pequediks'] = True
        if 'jpro_staff' in group_names:
            app_perms['can_access_jpro'] = True


    tenant_memberships = []
    current_tenant = getattr(request, 'tenant', None)

    if user.is_authenticated:
        tenant_memberships = TenantMembership.objects.select_related('tenant').filter(
            user=user,
            is_active=True,
            tenant__is_active=True,
        )

    return {
        'app_perms': app_perms,
        'tenant_memberships': tenant_memberships,
        'current_tenant': current_tenant,
    }
