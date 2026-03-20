from threading import local

from django.core.exceptions import ImproperlyConfigured
from django.db import models


_state = local()


def set_current_tenant(tenant):
    _state.tenant = tenant


def get_current_tenant():
    return getattr(_state, 'tenant', None)


def set_current_user(user):
    _state.user = user


def get_current_user():
    return getattr(_state, 'user', None)


class TenantAwareQuerySet(models.QuerySet):
    def for_current_tenant(self):
        tenant = get_current_tenant()
        if tenant is None:
            return self
        return self.filter(tenant=tenant)


class TenantAwareManager(models.Manager):
    def get_queryset(self):
        return TenantAwareQuerySet(self.model, using=self._db).for_current_tenant()


class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(
        'account.Tenant',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        editable=False,
        related_name='%(app_label)s_%(class)s_set',
    )

    objects = TenantAwareManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.tenant_id is None:
            tenant = get_current_tenant()
            if tenant is None:
                raise ImproperlyConfigured(
                    f'No hay tenant activo para guardar {self.__class__.__name__}.'
                )
            self.tenant = tenant
        super().save(*args, **kwargs)
