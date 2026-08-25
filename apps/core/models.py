from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    foto = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'Perfil {self.user.username}'


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
