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
        related_name='pusukids_staff',
        help_text=_("Link this coordinator profile to a Django user account to allow login.")
    )
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

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
        unique_together = [('tenant', 'name', 'surname')]

    def __str__(self):
        return self.name


class groupage(TenantAwareModel):
    name = models.CharField(max_length=8)
    description = models.CharField(max_length=16)

    class Meta:
        unique_together = [('tenant', 'name')]

    def __str__(self):
        return self.name


class child(TenantAwareModel):
    STATUS_ACTIVO = 'activo'
    STATUS_PROMOVIDO = 'promovido'
    STATUS_CHOICES = [
        (STATUS_ACTIVO, 'Activo'),
        (STATUS_PROMOVIDO, 'Promovido'),
    ]

    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    birthday = models.DateField(validators=[validate_date])
    groupage = models.ForeignKey(groupage, on_delete=models.PROTECT)
    parent_name = models.CharField(max_length=128, blank=True)
    contact_phone = models.CharField(max_length=16, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVO)

    class Meta:
        unique_together = [('tenant', 'name', 'surname')]

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


class fecha(TenantAwareModel):
    date = models.DateField(validators=[validate_date])
    week_no = models.IntegerField()

    class Meta:
        unique_together = [('tenant', 'date')]

    def __str__(self):
        return str(self.date)


class assistance(TenantAwareModel):
    child = models.ForeignKey(child, on_delete=models.PROTECT)
    date = models.ForeignKey(fecha, on_delete=models.PROTECT)
    group = models.ForeignKey(group, on_delete=models.PROTECT)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    attended = models.BooleanField()

    class Meta:
        unique_together = [('tenant', 'child', 'date')]

    def __str__(self):
        return f"{self.child.name} - {self.date.date}"


class weekinfo(TenantAwareModel):
    total_kids = models.IntegerField(default=0)
    total_servers = models.IntegerField(default=0)
    money_collected = models.FloatField(default=0.0)
    fecha = models.ForeignKey(fecha, on_delete=models.PROTECT)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(group, on_delete=models.PROTECT)

    def __str__(self):
        fecha_str = str(self.fecha.date) if self.fecha else "Sin Fecha"
        grupo_str = self.group.name if self.group else "Sin Grupo"
        return f"Info Semana: {fecha_str} - Grupo: {grupo_str}"


class expense(TenantAwareModel):
    description = models.CharField(max_length=64)
    amount = models.FloatField()
    fecha = models.ForeignKey(fecha, on_delete=models.PROTECT)
    reference = models.CharField(max_length=16)
    transdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.description


class GroupCoordinator(TenantAwareModel):
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    coordinator = models.ForeignKey(coordinator, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('tenant', 'group', 'coordinator')]
        verbose_name = "AsignaciÃ³n Grupo-Coordinador"
        verbose_name_plural = "Asignaciones Grupo-Coordinador"

    def __str__(self):
        return f"{self.group.name} - {self.coordinator.name} {self.coordinator.surname}"
