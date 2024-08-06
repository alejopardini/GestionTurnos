from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),
    path('turnos/', views.listar_turnos, name='listar_turnos'),
    path('turnos/crear/', views.crear_turno, name='crear_turno'),
    path('turnos/editar/<int:pk>/', views.editar_turno, name='editar_turno'),
]
