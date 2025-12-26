from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_time = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间", help_text="创建时间")
    updated_time = models.DateTimeField(
        auto_now=True, verbose_name="更新时间", help_text="更新时间")
    is_deleted = models.BooleanField(default=False,
                                     verbose_name='是否删除',
                                     help_text='是否删除')

    class Meta:
        abstract = True
