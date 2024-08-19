from django.db import models
from datetime import datetime, timedelta 

from pytz import timezone
from django.core.exceptions import ValidationError
from django.utils import timezone as django_timezone

def obtener_zona_horaria(usuario):
    # Lógica para obtener la zona horaria del usuario
    return 'America/Argentina/Buenos_Aires'

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    historial = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='media/archivos/', blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        nombres = self.nombre.split()
        apellidos = self.apellido.split()
        return ' '.join(n.capitalize() for n in nombres + apellidos)

    @property
    def edad(self):
        today = django_timezone.now().date()  # Usa django_timezone aquí
        if self.fecha_nacimiento:
            edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            return edad
        return None

    @property
    def ultima_consulta(self):
        from .models import Turno
        ultimo_turno = Turno.objects.filter(paciente=self).order_by('-fecha', '-hora').first()
        return ultimo_turno.fecha if ultimo_turno else 'Nunca'

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.DurationField(default=timedelta(hours=1))
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.paciente} - {self.fecha} {self.hora}'

    def clean(self):
    # Convertir fecha y hora a un objeto datetime consciente de la zona horaria
        if self.fecha is None or self.hora is None:
            raise ValidationError('La fecha y hora del turno no pueden ser nulas.')

    # Asegúrate de que `datetime` está correctamente importado
        from datetime import datetime

        tz = django_timezone.get_current_timezone()
        fecha_hora = django_timezone.make_aware(datetime.combine(self.fecha, self.hora), timezone=tz)

    # Validar que la fecha y hora no esté en el pasado
        ahora = django_timezone.now()
        if fecha_hora < ahora:
            raise ValidationError('La fecha y hora del turno no pueden estar en el pasado.')

    # Validar solapamiento de turnos
        start_time = fecha_hora
        end_time = start_time + self.duracion
    
        overlapping_turnos = Turno.objects.filter(
            fecha__lt=end_time.date(),
            hora__lt=end_time.time()
        ).exclude(pk=self.pk)
    
        if overlapping_turnos.exists():
            raise ValidationError('Ya existe un turno en el mismo horario.')
    
    # Validar que el turno esté en el rango permitido
        if not (8 <= fecha_hora.hour < 18):
            raise ValidationError('El turno debe estar entre las 8:00 y las 18:00.')

        if fecha_hora.hour == 12 and fecha_hora.minute >= 0:
            raise ValidationError('No se permiten turnos entre las 12:00 y las 14:00.')