"""
URL configuration for sistemaamigos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(('apps.core.urls', 'core'), namespace='core')),
    path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('gestion/clientes/', include(('apps.gestion.clientes.urls', 'clientes'), namespace='clientes')),
    path('gestion/servicios/', include(('apps.gestion.servicios.urls', 'servicios'), namespace='servicios')),
    path('gestion/empleados/', include(('apps.gestion.empleados.urls', 'empleados'), namespace='empleados')),
    path('gestion/sesiones/', include(('apps.gestion.sesiones.urls', 'sesiones'), namespace='sesiones')),
    path('gestion/pagos/', include(('apps.gestion.pagos.urls', 'pagos'), namespace='pagos')),
    path('gestion/agenda/', include(('apps.gestion.agenda.urls', 'agenda'), namespace='agenda')),
    path('gestion/eventos/', include(('apps.gestion.eventos.urls', 'eventos'), namespace='eventos')),
    path('gestion/finanzas/', include(('apps.gestion.finanzas.urls', 'finanzas'), namespace='finanzas')),
    path('gestion/reportes/', include(('apps.gestion.reportes.urls', 'reportes'), namespace='reportes')),
    path('gestion/permisos/', include(('apps.gestion.permisos.urls', 'permisos'), namespace='permisos')),
    path('secret-admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
