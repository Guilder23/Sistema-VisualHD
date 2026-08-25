from django.urls import path

from .views import (
    cambiar_contrasena,
    cerrar_sesion,
    editar_perfil,
    editar_usuario,
    eliminar_usuario,
    inicio,
    iniciar_sesion,
    perfil,
    robots_txt,
    registrar_usuario,
    sitemap_xml,
    subir_foto,
    toggle_bloqueo_usuario,
)

app_name = 'core'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro/', registrar_usuario, name='registro'),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('perfil/cambiar_contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
    path('perfil/subir_foto/', subir_foto, name='subir_foto'),
    path('usuarios/<int:user_id>/editar/', editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/bloqueo/', toggle_bloqueo_usuario, name='toggle_bloqueo_usuario'),
    path('usuarios/<int:user_id>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
]
