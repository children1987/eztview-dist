from django.db import models
from django.utils import timezone
from backend.apps.device_models.models import TfTemperatureMonitor, Transformer
from backend.apps.projects.models import OrgTree


class TransformerMonitor(models.Model):
    """
    变压器监测-变压器设备
    """
    org = models.ForeignKey(
        OrgTree,
        related_name='org_transformer_monitors',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    transformer = models.ForeignKey(
        Transformer,
        related_name='transformer_monitors',
        on_delete=models.CASCADE,
        verbose_name='变压器监测设备',
        help_text='变压器监测设备'
    )
    temperature_monitor = models.ForeignKey(
        TfTemperatureMonitor,
        related_name='temp_tf_monitors',
        on_delete=models.SET_NULL,
        verbose_name='变压器温度监测仪',
        help_text='变压器温度监测仪',
        null=True,
        blank=True
    )
    mode_type = models.CharField(
        verbose_name='变压器类型',
        help_text='变压器类型',
        max_length=30,
        null=True,
        blank=True
    )
    capacity = models.CharField(
        verbose_name='额定容量',
        help_text='额定容量',
        max_length=20,
        null=True,
        blank=True
    )
    code = models.CharField(
        verbose_name='出厂编号',
        help_text='出厂编号',
        max_length=30,
        null=True,
        blank=True
    )
    production_date = models.DateField(
        verbose_name='制造日期',
        help_text='制造日期',
        null=True,
        blank=True
    )
    manufacturer = models.CharField(
        verbose_name='厂商',
        help_text='厂商',
        max_length=100,
        null=True,
        blank=True
    )
    ordering = models.IntegerField(verbose_name='排序', default=0)
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '变压器监测-变压器监测设备'
        verbose_name_plural = verbose_name

