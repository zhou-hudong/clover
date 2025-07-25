


import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_delete, sender=Profile)
def delete_avatar_on_delete(sender, instance, **kwargs):
    """
    删除 Profile 实例时，移除 avatar 文件
    """
    if instance.avatar:
        avatar_path = instance.avatar.path
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)

@receiver(pre_save, sender=Profile)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    更新 avatar 前，删除旧文件
    """
    if not instance.pk:
        return

    try:
        old = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    old_file = old.avatar
    new_file = instance.avatar
    if old_file and old_file != new_file:
        old_path = old_file.path
        if os.path.isfile(old_path):
            os.remove(old_path)
