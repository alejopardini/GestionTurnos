# apps.py
from django.apps import AppConfig

class GestionTurnosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_turnos'

    def ready(self):
        # Importar el módulo de señales para que se ejecute cuando se inicien las migraciones
        import gestion_turnos.signals
