from django.db import models
from django.utils import timezone


class Area(models.Model):
    """
    行政区域，地区
    """

    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区划')
    city_id = models.CharField(verbose_name='用于请求天气的id', blank=True, null=True, max_length=30)

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        obj = self.parent
        name = self.name
        while obj:
            if obj.name not in name:
                name = f"{obj.name} {name}"
            obj = obj.parent
        return name

    def get_full_name(self):
        return str(self)

