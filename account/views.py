from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from .middleware import TenantMiddleware
from .models import TenantMembership


@login_required
def switch_tenant(request, tenant_id):
    membership = get_object_or_404(
        TenantMembership.objects.select_related('tenant'),
        user=request.user,
        tenant_id=tenant_id,
        is_active=True,
        tenant__is_active=True,
    )
    request.session[TenantMiddleware.SESSION_KEY] = membership.tenant_id
    messages.success(request, f"Tenant activo cambiado a {membership.tenant.name}.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))
