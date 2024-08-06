from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente, Turno
from .forms import PacienteForm, TurnoForm
from .utils import send_whatsapp_message

def inicio(request):
    return render(request, 'gestion_turnos/inicio.html')

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
    turnos = Turno.objects.all()
    return render(request, 'gestion_turnos/listar_turnos.html', {'turnos': turnos})

def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
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