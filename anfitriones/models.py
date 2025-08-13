from django.db import models

# Create your models here.

class Coordinator(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        unique_together = ('name', 'surname')


class Group(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.name
"""  """
class Server(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        unique_together = ('name', 'surname')

class Ministry(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    

class Assistance(models.Model):
    class ServiceChoices(models.TextChoices):
        PRIMERO = 'PRI', 'Primero'
        SEGUNDO = 'SEG', 'Segundo'
        TERCERO = 'TER', 'Tercero'

    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    date = models.DateField()
    starthour = models.TimeField()
    service = models.CharField(
        max_length=3,
        choices=ServiceChoices.choices,
        default=ServiceChoices.PRIMERO,
    )
    attended = models.BooleanField()

    def __str__(self):
         return f"{self.server} - {self.date} ({self.get_service_display()})"

    class Meta:
        unique_together = ('server', 'date', 'service')

class Attendance(models.Model):
    """Modelo para registrar la asistencia y estadísticas de un grupo en una fecha."""
    coordinator = models.ForeignKey(Coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    ministry = models.ForeignKey(Ministry, on_delete=models.PROTECT)
    date = models.DateField()
    attended = models.BooleanField()
    adults = models.PositiveIntegerField(default=0, help_text="Número de adultos")
    youngs = models.PositiveIntegerField(default=0, help_text="Número de jóvenes")
    children = models.PositiveIntegerField(default=0, help_text="Número de niños")
    autos = models.PositiveIntegerField(default=0, help_text="Número de autos")
    note = models.TextField(blank=True, help_text="Observaciones o notas adicionales")

    @property
    def total(self):
        """Suma la asistencia de adultos, jóvenes y niños."""
        return self.adults + self.youngs + self.children

    def __str__(self):
        return f"Asistencia de {self.group.name} el {self.date}"
    
    