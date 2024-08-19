from django import forms
from .models import Paciente, Turno
from django.utils import timezone
from datetime import datetime
import pytz

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido','telefono', 'email', 'historial', 'archivo', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})
        }
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento and fecha_nacimiento > timezone.now().date():
            raise forms.ValidationError("La fecha de nacimiento no puede ser posterior a la fecha actual.")
        return fecha_nacimiento


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['paciente', 'descripcion', 'fecha', 'hora']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha and hora:
            # Combina fecha y hora en un solo objeto datetime
            fecha_hora = datetime.combine(fecha, hora)
            # Convertir fecha_hora a la zona horaria de tu aplicación
            tz = pytz.timezone('America/Argentina/Buenos_Aires')
            fecha_hora = tz.localize(fecha_hora)  # Convertir a offset-aware

            # Obtener la hora actual y convertirla a la misma zona horaria
            ahora = timezone.now()
            ahora = tz.localize(ahora.replace(tzinfo=None))  # Convertir ahora a offset-aware

            if fecha_hora < ahora:
                raise forms.ValidationError("No se pueden agendar turnos en fechas pasadas.")
            if fecha_hora.weekday() >= 5:  # Fin de semana
                raise forms.ValidationError("Los turnos solo se pueden agendar de lunes a viernes.")
            if not (8 <= fecha_hora.hour < 12 or 14 <= fecha_hora.hour < 18):
                raise forms.ValidationError("Los turnos deben estar entre 8:00-12:00 o 14:00-18:00.")
            if Turno.objects.filter(fecha=fecha, hora=hora).exists():
                raise forms.ValidationError("Ya existe un turno en este horario.")

        return cleaned_data
