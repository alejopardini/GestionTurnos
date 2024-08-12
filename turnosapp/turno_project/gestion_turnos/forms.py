from django import forms
from .models import Paciente, Turno
from datetime import datetime, time, timedelta
import pytz

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'telefono', 'email', 'historial']

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['paciente', 'fecha_hora', 'descripcion']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_hora'].widget.attrs.update({
            'min': self.get_min_datetime(),
            'max': self.get_max_datetime(),
        })

    def get_min_datetime(self):
        now = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
        return now.replace(hour=8, minute=0, second=0, microsecond=0).isoformat()

    def get_max_datetime(self):
        now = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
        return now.replace(hour=18, minute=0, second=0, microsecond=0).isoformat()

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora:
            if fecha_hora.weekday() >= 5:  # Fin de semana
                raise forms.ValidationError("Los turnos solo se pueden agendar de lunes a viernes.")
            if not (time(8, 0) <= fecha_hora.time() <= time(12, 0) or time(14, 0) <= fecha_hora.time() <= time(18, 0)):
                raise forms.ValidationError("Los turnos deben estar entre 8:00-12:00 o 14:00-18:00.")
            # Verificar si el horario está ocupado
            if Turno.objects.filter(fecha_hora=fecha_hora).exists():
                raise forms.ValidationError("Ya existe un turno en este horario.")
        return fecha_hora
