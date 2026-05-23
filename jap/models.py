from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.tenant import TenantAwareModel


def validate_date(value):
    try:
        value.strftime('%Y-%m-%d')
    except ValueError as e:
        raise ValidationError(str(e))


class coordinator(TenantAwareModel):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("user account"),
        related_name='jap_staff',
        help_text=_("Link this coordinator profile to a Django user account to allow login.")
    )
    name = models.CharField(_("name"), max_length=128)
    surname = models.CharField(_("surname"), max_length=128)

    def __str__(self):
        return f"{self.name} {self.surname}"


class group(TenantAwareModel):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64)

    class Meta:
        unique_together = [('tenant', 'name')]

    def __str__(self):
        return self.name


class server(TenantAwareModel):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(group, on_delete=models.PROTECT)

    class Meta:
        unique_together = [('tenant', 'name')]

    def __str__(self):
        return self.name


class child(TenantAwareModel):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('promovido', 'Promovido'),
    ]
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    birthday = models.DateField(validators=[validate_date])
    parent_name = models.CharField(max_length=128, blank=True)
    contact_phone = models.CharField(max_length=16, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='activo',
        verbose_name='Estado'
    )

    class Meta:
        unique_together = [('tenant', 'name')]

    @property
    def calculated_age(self):
        if not self.birthday:
            return None
        today = date.today()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    def __str__(self):
        return f"{self.name} {self.surname}"


class assistance(TenantAwareModel):
    child = models.ForeignKey(child, on_delete=models.PROTECT)
    date = models.DateField()
    group = models.ForeignKey(group, on_delete=models.PROTECT)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    attended = models.BooleanField()

    class Meta:
        unique_together = [('tenant', 'child', 'date')]

    def __str__(self):
        return f"{self.child.name} - {self.date}"


class GroupCoordinator(TenantAwareModel):
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    coordinator = models.ForeignKey(coordinator, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('tenant', 'group', 'coordinator')]
        verbose_name = "AsignaciÃ³n Grupo-Coordinador (Cuna)"
        verbose_name_plural = "Asignaciones Grupo-Coordinador (Cuna)"

    def __str__(self):
        return f"{self.group.name} - {self.coordinator.name} {self.coordinator.surname}"
