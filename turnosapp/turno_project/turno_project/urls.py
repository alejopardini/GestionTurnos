from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_turnos/', include('gestion_turnos.urls')),
    path('', include('gestion_turnos.urls')),  # Esto establece la página de inicio
]



