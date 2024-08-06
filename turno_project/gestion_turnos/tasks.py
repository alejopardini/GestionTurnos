from celery import shared_task
from twilio.rest import Client
from django.conf import settings
from .models import Turno
from datetime import datetime, timedelta
import pytz

@shared_task
def enviar_recordatorios():
    # Configuración de Twilio
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    
    # Configuración de zona horaria
    ahora = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
    maniana = ahora + timedelta(days=1)
    proximas_horas = ahora + timedelta(hours=1)

    # Filtrar turnos
    turnos_maniana = Turno.objects.filter(fecha_hora__date=maniana.date())
    turnos_proximas_horas = Turno.objects.filter(fecha_hora__range=(proximas_horas, proximas_horas + timedelta(hours=1)))

    # Enviar recordatorios para turnos de mañana
    for turno in turnos_maniana:
        mensaje = f'Recordatorio: tiene un turno mañana a las {turno.fecha_hora.strftime("%H:%M")}'
        try:
            client.messages.create(
                body=mensaje,
                from_='whatsapp:+14155238886',  # Número de Twilio para WhatsApp
                to=f'whatsapp:{turno.paciente.telefono}'
            )
        except Exception as e:
            print(f'Error al enviar mensaje a {turno.paciente.telefono}: {e}')

    # Enviar recordatorios para turnos en las próximas horas
    for turno in turnos_proximas_horas:
        mensaje = f'Recordatorio: tiene un turno en una hora a las {turno.fecha_hora.strftime("%H:%M")}'
        try:
            client.messages.create(
                body=mensaje,
                from_='whatsapp:+14155238886',  # Número de Twilio para WhatsApp
                to=f'whatsapp:{turno.paciente.telefono}'
            )
        except Exception as e:
            print(f'Error al enviar mensaje a {turno.paciente.telefono}: {e}')
