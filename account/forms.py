from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import TenantMembership


class TenantAwareAuthenticationForm(AuthenticationForm):
    tenant = forms.ModelChoiceField(
        queryset=TenantMembership.objects.none(),
        label='Iglesia',
        empty_label='Selecciona una iglesia',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    error_messages = {
        'invalid_login': 'Usuario o contrasena incorrectos para la iglesia seleccionada.',
        'inactive': 'Esta cuenta esta inactiva.',
        'invalid_tenant': 'No tienes acceso a la iglesia seleccionada.',
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['tenant'].queryset = (
            TenantMembership.objects.select_related('tenant')
            .filter(is_active=True, tenant__is_active=True)
            .values_list('tenant__id', flat=True)
        )

        from .models import Tenant

        self.fields['tenant'].queryset = Tenant.objects.filter(
            is_active=True,
            memberships__is_active=True,
        ).distinct().order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        tenant = cleaned_data.get('tenant')
        user = self.get_user()

        if tenant and user:
            has_membership = TenantMembership.objects.filter(
                user=user,
                tenant=tenant,
                is_active=True,
                tenant__is_active=True,
            ).exists()
            if not has_membership:
                raise ValidationError(
                    self.error_messages['invalid_tenant'],
                    code='invalid_tenant',
                )

        return cleaned_data
