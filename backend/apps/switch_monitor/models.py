from django.db import models
from django.utils import timezone
from backend.apps.custom_perm.models import BaseDeviceNodeModel
from backend.apps.device_models.models import SwitchMonitor
from backend.apps.projects.models import OrgTree


class SwitchMonitorNode(BaseDeviceNodeModel):
    """
    开关监控 - 树结构
    """

    org = models.ForeignKey(
        OrgTree,
        related_name='org_switch_monitors',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    switch_monitor = models.ForeignKey(
        SwitchMonitor,
        related_name='switch_monitor_nodes',
        on_delete=models.CASCADE,
        verbose_name='开关监控模型设备',
        help_text='开关监控模型设备',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '开关监控-树结构'
        verbose_name_plural = verbose_name


class SwitchDevice(models.Model):
    """
    开关监控应用设备
    """
    switch_monitor = models.ForeignKey(
        SwitchMonitor,
        related_name='switch_devices',
        on_delete=models.CASCADE,
        verbose_name='开关监控模型设备',
        help_text='开关监控模型设备'
    )
    node = models.OneToOneField(
        SwitchMonitorNode,
        related_name='node_switch_monitor',
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
        verbose_name = '开关监控应用设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.node.name

