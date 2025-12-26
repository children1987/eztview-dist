from django.db import models
from django.utils import timezone

from backend.apps.device_models.models import HiddenDangerMonitor, \
    PowerSource, ElectricMeter
from backend.apps.projects.models import OrgTree


class ElHiddenDangerMonitor(models.Model):
    """
    电能看板-隐患监测
    """
    org = models.ForeignKey(
        OrgTree,
        related_name='org_hidden_danger_monitors',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
    )
    hidden_danger_monitor = models.ForeignKey(
        HiddenDangerMonitor,
        related_name='el_hidden_danger_monitors',
        on_delete=models.CASCADE,
        verbose_name='隐患监测设备',
        help_text='隐患监测备'
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '电能看板-隐患监测'
        verbose_name_plural = verbose_name


class ElPowerSource(models.Model):
    """
    电能看板-电源
    """
    org = models.ForeignKey(
        OrgTree,
        related_name='org_power_sources',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
    )
    power_source = models.ForeignKey(
        PowerSource,
        related_name='el_power_sources',
        on_delete=models.CASCADE,
        verbose_name='电源设备',
        help_text='电源设备'
    )
    ordering = models.IntegerField(
        verbose_name='排序',
        help_text='排序',
        db_index=True,
        default=0
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '电能看板-电源'
        verbose_name_plural = verbose_name


class ElectricMeterLoad(models.Model):
    """
    电能看板-负载
    """
    org = models.ForeignKey(
        OrgTree,
        related_name='org_el_loads',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
    )
    electric_meter = models.ForeignKey(
        ElectricMeter,
        related_name='el_meter_loads',
        on_delete=models.CASCADE,
        verbose_name='电表模型',
        help_text='电表模型'
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '电能看板-负载'
        verbose_name_plural = verbose_name


