# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

@receiver(post_migrate)
def create_periodic_task(sender, **kwargs):
    if sender.name == 'gestion_turnos':  # Verificar que la señal se ejecute solo para esta aplicación
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
