from django.shortcuts import redirect
from django.urls import reverse

from .models import TenantMembership
from .tenant import set_current_tenant, set_current_user


class TenantMiddleware:
    SESSION_KEY = 'active_tenant_id'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(getattr(request, 'user', None))
        tenant = None

        if getattr(request, 'user', None) and request.user.is_authenticated:
            memberships = TenantMembership.objects.select_related('tenant').filter(
                user=request.user,
                is_active=True,
                tenant__is_active=True,
            )
            selected_tenant_id = request.session.get(self.SESSION_KEY)
            membership = memberships.filter(tenant_id=selected_tenant_id).first()

            if membership is None:
                membership = memberships.order_by('-is_default', 'tenant__name').first()
                if membership:
                    request.session[self.SESSION_KEY] = membership.tenant_id

            if membership:
                tenant = membership.tenant
            elif request.path not in {
                reverse('account:logout'),
                reverse('account:login'),
            } and not request.user.is_superuser:
                return redirect('account:login')

        request.tenant = tenant
        set_current_tenant(tenant)
        response = self.get_response(request)
        set_current_tenant(None)
        set_current_user(None)
        return response
