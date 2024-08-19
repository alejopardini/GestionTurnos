from django.db import migrations, models
from datetime import time

class Migration(migrations.Migration):

    dependencies = [
        ('gestion_turnos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='hora',
            field=models.TimeField(default=time(8, 0)),
        ),
        migrations.RemoveField(
            model_name='turno',
            name='fecha_hora',
        ),
    ]
