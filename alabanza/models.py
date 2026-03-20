from django.db import models
from account.tenant import TenantAwareModel
 # Create your models here. 

class Coordinator(TenantAwareModel):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)     
    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        unique_together = ('tenant', 'name', 'surname')


class Group(TenantAwareModel):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('tenant', 'name')

class Server(TenantAwareModel):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        unique_together = ('tenant', 'name', 'surname')

class Assistance(TenantAwareModel):
    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    date = models.DateField()
    # Los campos group y coordinator se eliminan asumiendo que la asistencia
    # siempre corresponde al grupo y coordinador asignados al servidor.
    # Si un servidor puede asistir bajo diferentes grupos/coordinadores temporalmente,
    # estos campos deberían mantenerse.
    attended = models.BooleanField()

    def __str__(self):
         return f"{self.server} - {self.date}"

                

        
                     
