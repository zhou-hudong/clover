


import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Service

@receiver(post_delete, sender=Service)
def delete_service_image_on_delete(sender, instance, **kwargs):
    """
    当 Service 实例被删除后，自动删除它的 image 文件
    """
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)

@receiver(pre_save, sender=Service)
def delete_old_service_image_on_change(sender, instance, **kwargs):
    """
    当 Service.image 被更新（换了张新图）前，删除旧文件
    """
    if not instance.pk:
        return  # 新创建，无需处理

    try:
        old_instance = Service.objects.get(pk=instance.pk)
    except Service.DoesNotExist:
        return

    old_file = old_instance.image
    new_file = instance.image
    # 如果换了新图，就删除旧图
    if old_file and old_file != new_file:
        old_path = old_file.path
        if os.path.isfile(old_path):
            os.remove(old_path)
