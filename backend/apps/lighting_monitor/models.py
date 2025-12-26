from django.db import models
from django.utils import timezone
from backend.apps.custom_perm.models import BaseDeviceNodeModel
from backend.apps.device_models.models import LightMonitor
from backend.apps.projects.models import OrgTree


class LightMonitorNode(BaseDeviceNodeModel):
    """
    照明系统 - 树结构
    """

    org = models.ForeignKey(
        OrgTree,
        related_name='org_light_monitors',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    light_monitor = models.ForeignKey(
        LightMonitor,
        related_name='lighting_monitor_nodes',
        on_delete=models.CASCADE,
        verbose_name='设备模型照明设备',
        help_text='设备模型照明设备',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '照明系统-树结构'
        verbose_name_plural = verbose_name


class LightDevice(models.Model):
    """
    照明系统 -- 设备
    """
    light_monitor = models.ForeignKey(
        LightMonitor,
        related_name='lighting_devices',
        on_delete=models.CASCADE,
        verbose_name='设备模型照明设备',
        help_text='设备模型照明设备'
    )
    node = models.OneToOneField(
        LightMonitorNode,
        related_name='node_light_monitor',
        on_delete=models.CASCADE,
        verbose_name='分组',
        help_text='分组',
        null=True,
        blank=True,
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '照明系统-设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.node.name

