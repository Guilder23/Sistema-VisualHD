from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from xml.sax.saxutils import escape

from .models import UserProfile


def get_home_redirect(user):
    return 'dashboard:dashboard'


def inicio(request):
    if request.user.is_authenticated:
        return redirect(get_home_redirect(request.user))
    return render(request, 'core/inicio.html')


def robots_txt(request):
	sitemap_url = f'{settings.PUBLIC_SITE_URL}{reverse("core:sitemap")}'
	content = '\n'.join([
		'User-agent: *',
		'Allow: /',
		'Disallow: /login/',
		'Disallow: /secret-admin/',
		'Disallow: /gestion/',
		'Disallow: /dashboard/',
		'Sitemap: ' + sitemap_url,
		'',
	])
	return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
	public_urls = [
		f'{settings.PUBLIC_SITE_URL}{reverse("core:inicio")}',
	]
	url_entries = ''.join(
		f'<url><loc>{escape(url)}</loc><changefreq>weekly</changefreq><priority>{priority}</priority></url>'
		for url, priority in ((public_urls[0], '1.0'),)
	)
	content = (
		'<?xml version="1.0" encoding="UTF-8"?>'
		'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
		f'{url_entries}'
		'</urlset>'
	)
	return HttpResponse(content, content_type='application/xml')


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect(get_home_redirect(request.user))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Usuario o contrasena incorrectos.')
            return render(request, 'auth/login.html')

        if not user.is_active:
            messages.error(request, 'Tu cuenta esta bloqueada. Comunicate con el administrador.')
            return render(request, 'auth/login.html')

        login(request, user)
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect(get_home_redirect(user))

    return render(request, 'auth/login.html')


@login_required
def cerrar_sesion(request):
	logout(request)
	return redirect('core:inicio')


@login_required
def perfil(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'core/perfil.html', {'user_profile': profile})


@login_required
def editar_perfil(request):
    if request.method != 'POST':
        return redirect('core:perfil')

    user = request.user
    email = request.POST.get('email', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()

    if email:
        user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    messages.success(request, 'Datos de perfil actualizados.')
    return redirect('core:perfil')


@login_required
def cambiar_contrasena(request):
    if request.method != 'POST':
        return redirect('core:perfil')

    user = request.user
    current = request.POST.get('current_password', '')
    new1 = request.POST.get('new_password1', '')
    new2 = request.POST.get('new_password2', '')

    if not current or not new1 or not new2:
        messages.error(request, 'Completa los 3 campos requeridos para cambiar la contraseña.')
        return redirect('core:perfil')

    if not user.check_password(current):
        messages.error(request, 'La contraseña actual es incorrecta.')
        return redirect('core:perfil')

    if new1 != new2:
        messages.error(request, 'Las nuevas contraseñas no coinciden.')
        return redirect('core:perfil')

    user.set_password(new1)
    user.save()
    update_session_auth_hash(request, user)
    messages.success(request, 'Contraseña actualizada correctamente.')
    return redirect('core:perfil')


@login_required
def subir_foto(request):
    if request.method != 'POST':
        return redirect('core:perfil')

    foto = request.FILES.get('foto')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if foto:
        profile.foto = foto
        profile.save()
        messages.success(request, 'Foto de perfil actualizada.')
    else:
        messages.error(request, 'No se recibió archivo.')

    return redirect('core:perfil')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def registrar_usuario(request):
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		password2 = request.POST.get('password2', '')
		is_admin = request.POST.get('is_admin') == 'on'

		if not username or not password:
			messages.error(request, 'Usuario y contrasena son obligatorios.')
			return redirect('core:registro')

		if password != password2:
			messages.error(request, 'Las contrasenas no coinciden.')
			return redirect('core:registro')

		if User.objects.filter(username=username).exists():
			messages.error(request, 'El nombre de usuario ya existe.')
			return redirect('core:registro')

		user = User.objects.create_user(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password,
		)
		user.is_staff = is_admin
		user.save()

		messages.success(request, 'Usuario creado correctamente.')
		return redirect('core:registro')

	q = request.GET.get('q', '').strip()
	rol = request.GET.get('rol', '').strip()
	estado = request.GET.get('estado', '').strip()

	usuarios_qs = User.objects.order_by('-date_joined')
	if q:
		usuarios_qs = usuarios_qs.filter(
			Q(username__icontains=q)
			| Q(first_name__icontains=q)
			| Q(last_name__icontains=q)
			| Q(email__icontains=q)
		)

	if rol == 'admin':
		usuarios_qs = usuarios_qs.filter(is_staff=True)
	elif rol == 'usuario':
		usuarios_qs = usuarios_qs.filter(is_staff=False)

	if estado == 'activo':
		usuarios_qs = usuarios_qs.filter(is_active=True)
	elif estado == 'bloqueado':
		usuarios_qs = usuarios_qs.filter(is_active=False)

	paginator = Paginator(usuarios_qs, 10)
	page_number = request.GET.get('page')
	usuarios = paginator.get_page(page_number)

	return render(
		request,
		'auth/registro.html',
		{
			'usuarios': usuarios,
			'q': q,
			'rol': rol,
			'estado': estado,
		},
	)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_usuario(request, user_id):
	objetivo = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		if objetivo.is_superuser and not request.user.is_superuser:
			messages.error(request, 'No tienes permiso para editar este usuario.')
			return redirect('core:registro')

		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		is_admin = request.POST.get('is_admin') == 'on'

		if not username:
			messages.error(request, 'El usuario es obligatorio.')
			return redirect('core:registro')

		if User.objects.exclude(id=objetivo.id).filter(username=username).exists():
			messages.error(request, 'Ese nombre de usuario ya existe.')
			return redirect('core:registro')

		objetivo.username = username
		objetivo.email = email
		objetivo.first_name = first_name
		objetivo.last_name = last_name
		objetivo.is_staff = is_admin

		password = request.POST.get('password', '')
		password2 = request.POST.get('password2', '')
		if password or password2:
			if password != password2:
				messages.error(request, 'Las contrasenas no coinciden.')
				return redirect('core:registro')
			objetivo.set_password(password)

		objetivo.save()
		messages.success(request, 'Usuario actualizado correctamente.')

	return redirect('core:registro')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def toggle_bloqueo_usuario(request, user_id):
	objetivo = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		if objetivo == request.user:
			messages.error(request, 'No puedes bloquear tu propio usuario.')
			return redirect('core:registro')

		if objetivo.is_superuser and not request.user.is_superuser:
			messages.error(request, 'No tienes permiso para bloquear este usuario.')
			return redirect('core:registro')

		objetivo.is_active = not objetivo.is_active
		objetivo.save(update_fields=['is_active'])
		messages.success(
			request,
			f"Usuario {'bloqueado' if not objetivo.is_active else 'desbloqueado'} correctamente.",
		)

	return redirect('core:registro')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_usuario(request, user_id):
	objetivo = get_object_or_404(User, id=user_id)

	if request.method == 'POST':
		if objetivo == request.user:
			messages.error(request, 'No puedes eliminar tu propio usuario.')
			return redirect('core:registro')

		if objetivo.is_superuser and not request.user.is_superuser:
			messages.error(request, 'No tienes permiso para eliminar este usuario.')
			return redirect('core:registro')

		objetivo.delete()
		messages.success(request, 'Usuario eliminado correctamente.')

	return redirect('core:registro')
