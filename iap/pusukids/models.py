from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

def validate_date(value):
    try:
        value.strftime('%Y-%m-%d')  # Forzar validación
    except ValueError as e:
        raise ValidationError(str(e))
    

class coordinator(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("user account"),
        related_name='pusukids_staff', # related_name to avoid clashes
        help_text=_("Link this coordinator profile to a Django user account to allow login.")
    )
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)     
    def __str__(self):
        return f"{self.name} {self.surname}"


class group(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name

class server(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(group, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
        
class groupage(models.Model):
    name = models.CharField(max_length=8)
    description = models.CharField(max_length=16)
    
    def __str__(self):
        return self.name

class child(models.Model):
    STATUS_ACTIVO = 'activo'
    STATUS_PROMOVIDO = 'promovido'
    STATUS_CHOICES = [
        (STATUS_ACTIVO, 'Activo'),
        (STATUS_PROMOVIDO, 'Promovido'),
    ]

    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    birthday = models.DateField(validators=[validate_date]) # El campo clave a probar
    # Usaremos groupage también para simular la ForeignKey
    groupage = models.ForeignKey(groupage, on_delete=models.PROTECT)
    parent_name = models.CharField(max_length=128, blank=True) # Hacemos algunos opcionales
    contact_phone = models.CharField(max_length=16, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVO)

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

    class Meta:
        unique_together = [['name', 'surname']]

class fecha(models.Model):
    date = models.DateField(validators=[validate_date], unique=True)
    week_no = models.IntegerField()
    
    def __str__(self):
        return str(self.date)
        
class assistance(models.Model):
    # kid = models.ForeignKey(kid, on_delete=models.PROTECT) # <-- Línea antigua
    child = models.ForeignKey(child, on_delete=models.PROTECT) # <-- CAMBIAR A child
    date = models.ForeignKey(fecha, on_delete=models.PROTECT)
    group = models.ForeignKey(group, on_delete=models.PROTECT)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    attended = models.BooleanField()

    def __str__(self):
         # Actualizar también aquí si es necesario
         return f"{self.child.name} - {str(self.date.date)}"

    class Meta:
        unique_together = [['child', 'date']]

                
class weekinfo(models.Model):
    # --- CORREGIDO ---
    # Decide qué debe ser total_kids. Probablemente un entero.
    total_kids = models.IntegerField(default=0) # Asumiendo que es un contador, necesita () y default
    total_servers = models.IntegerField(default=0) # Necesita () y default
    money_collected = models.FloatField(default=0.0) # Necesita () y default
    # --- FIN CORRECCIÓN ---
    fecha = models.ForeignKey(fecha, on_delete=models.PROTECT)
    coordinator = models.ForeignKey(coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(group, on_delete=models.PROTECT)

    def __str__(self):
        # Mejor devolver un string formateado y seguro
        fecha_str = str(self.fecha.date) if self.fecha else "Sin Fecha"
        grupo_str = self.group.name if self.group else "Sin Grupo"
        return f"Info Semana: {fecha_str} - Grupo: {grupo_str}"
        
class expense(models.Model):
    description = models.CharField(max_length=64)
    amount = models.FloatField()
    fecha = models.ForeignKey(fecha, on_delete=models.PROTECT)    
    reference = models.CharField(max_length=16)
    transdate = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.description
        
class GroupCoordinator(models.Model):
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    coordinator = models.ForeignKey(coordinator, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['group', 'coordinator']]
        verbose_name = "Asignación Grupo-Coordinador"
        verbose_name_plural = "Asignaciones Grupo-Coordinador"

    def __str__(self):
        return f"{self.group.name} - {self.coordinator.name} {self.coordinator.surname}"

                    