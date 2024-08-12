from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente, Turno
from .forms import PacienteForm, TurnoForm
from .utils import send_whatsapp_message
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse

def inicio(request):
    today = timezone.now().date()  # Obtén solo la fecha, no la hora
    start_of_week = today - timedelta(days=today.weekday())  # Empieza desde el primer día de la semana
    num_weeks = 2
    num_days_per_week = 7

    # Calcula el calendario
    calendar = []
    for week in range(num_weeks):
        week_days = []
        for day in range(num_days_per_week):
            day_date = start_of_week + timedelta(days=day + week * num_days_per_week)
            week_days.append(day_date)
        calendar.append(week_days)

    # Obtener todos los turnos dentro del rango de fechas
    end_of_period = start_of_week + timedelta(weeks=num_weeks)
    turnos = Turno.objects.filter(fecha_hora__date__range=(start_of_week, end_of_period))

    # Convertir turnos a formato JSON adecuado para FullCalendar
    turnos_json = []
    for turno in turnos:
        turnos_json.append({
            'title': f'{turno.paciente.nombre}: {turno.descripcion}',
            'start': turno.fecha_hora.isoformat(),  # Usa el formato ISO 8601
        })

    context = {
        'calendar': calendar,
        'turnos': turnos_json,
    }
    return render(request, 'gestion_turnos/inicio.html', context)

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'gestion_turnos/listar_pacientes.html', {'pacientes': pacientes})

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'gestion_turnos/crear_paciente.html', {'form': form})

def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'gestion_turnos/editar_paciente.html', {'form': form})

def listar_turnos(request):
    turnos = Turno.objects.all().order_by('fecha_hora')
    return render(request, 'gestion_turnos/listar_turnos.html', {'turnos': turnos})

def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
        else:
            # Si hay errores en el formulario, vuelve a mostrar el formulario con los errores
            return render(request, 'gestion_turnos/crear_turno.html', {'form': form})
    else:
        form = TurnoForm()
    return render(request, 'gestion_turnos/crear_turno.html', {'form': form})

def editar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'gestion_turnos/editar_turno.html', {'form': form})

def send_reminder(request):
    to = '+1234567890'  # Número de teléfono del destinatario en formato internacional
    body = 'Este es un recordatorio de tu cita.'
    message_sid = send_whatsapp_message(to, body)
    return HttpResponse(f'Mensaje enviado con SID: {message_sid}')
