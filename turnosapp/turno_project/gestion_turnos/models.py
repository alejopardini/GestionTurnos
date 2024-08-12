from django.db import models
from datetime import timedelta 
from pytz import timezone
from django.core.exceptions import ValidationError

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

    def clean(self):
        # Validar solapamiento de turnos
        start_time = self.fecha_hora
        end_time = start_time + self.duracion
        
        overlapping_turnos = Turno.objects.filter(
            fecha_hora__lt=end_time,
            fecha_hora__gte=start_time
        ).exclude(pk=self.pk)
        
        if overlapping_turnos.exists():
            raise ValidationError('Ya existe un turno en el mismo horario.')
        
        # Validar que el turno esté en el rango permitido
        if not (self.fecha_hora.hour >= 8 and self.fecha_hora.hour < 18):
            raise ValidationError('El turno debe estar entre las 8:00 y las 18:00.')

        if self.fecha_hora.hour == 12 and self.fecha_hora.minute >= 0:
            raise ValidationError('No se permiten turnos entre las 12:00 y las 14:00.')
