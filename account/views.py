from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from .forms import TenantAwareAuthenticationForm
from .middleware import TenantMiddleware
from .models import TenantMembership


class TenantLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = TenantAwareAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        tenant = form.cleaned_data.get('tenant')
        if tenant:
            self.request.session[TenantMiddleware.SESSION_KEY] = tenant.id
        return response


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
