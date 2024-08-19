from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_turnos/', include('gestion_turnos.urls')),
    path('', include('gestion_turnos.urls')),  # Esto establece la página de inicio
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



