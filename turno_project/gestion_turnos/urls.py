from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('turnos/', views.listar_turnos, name='listar_turnos'),
    path('turnos/crear/', views.crear_turno, name='crear_turno'),
    path('turnos/editar/<int:pk>/', views.editar_turno, name='editar_turno'),
    path('borrar_turno/<int:pk>/', views.borrar_turno, name='borrar_turno'),
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('paciente/<int:pk>/', views.detalle_paciente, name='detalle_paciente'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/borrar/<int:pk>/', views.borrar_paciente, name='borrar_paciente'),
    path('pacientes/editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),
    path('enviar-recordatorio/', views.send_reminder, name='send_reminder'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)