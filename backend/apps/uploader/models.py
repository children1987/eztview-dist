import os

from django.conf import settings
from django.db import models
from django.utils import timezone


def content_file_name(instance, filename):
    upload_dir = os.path.join('uploads', instance.belong_to)
    if not settings.IS_USE_COS:
        file_dir = os.path.join('media', upload_dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    return os.path.join(upload_dir, filename)


class FileObject(models.Model):
    file = models.FileField(verbose_name='文件对象', help_text='form-data',
                            upload_to=content_file_name)
    created_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间',
                                        default=timezone.now)
    belong_to = models.CharField(verbose_name='文件归属',
                                 help_text='文件归属', max_length=100)

    file_info = models.JSONField(
        verbose_name='文件信息',
        help_text='文件信息',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = verbose_name
