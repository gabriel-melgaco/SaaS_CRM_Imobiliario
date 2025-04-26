from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from authentication.models import TenantUser

@receiver(post_save, sender=TenantUser)
def change_permission_group(sender, instance, **kwargs):
    user = instance.user

    user.groups.clear()

    if instance.function == 'admin':
        group, _ = Group.objects.get_or_create(name='admin')
        user.groups.add(group)
    elif instance.function == 'recursos_humanos':
        group, _ = Group.objects.get_or_create(name='recursos_humanos')
        user.groups.add(group)
    elif instance.function == 'corretor':
        group, _ = Group.objects.get_or_create(name='corretor')
        user.groups.add(group)
