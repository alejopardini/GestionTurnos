from django.db import models
from datetime import timedelta 
from pytz import timezone

def obtener_zona_horaria(usuario):
    # Lógica para obtener la zona horaria del usuario
    return 'America/Argentina/Buenos_Aires'


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    historial = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    duracion = models.DurationField(default=timedelta(hours=1))
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.paciente} - {self.fecha_hora}'
