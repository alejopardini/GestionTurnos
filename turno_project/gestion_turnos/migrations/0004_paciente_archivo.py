# Generated by Django 5.0.7 on 2024-08-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_turnos', '0003_turno_fecha_alter_turno_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
    ]
