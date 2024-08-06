# apps.py
from django.apps import AppConfig
import json

class GestionTurnosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_turnos'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule

        # Crear un intervalo de tiempo
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )

        # Crear una tarea periódica
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Enviar recordatorios de turnos',
            task='gestion_turnos.tasks.enviar_recordatorios',
            args=json.dumps([]),
        )
