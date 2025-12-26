
from django.db import models
from django.utils import timezone

from backend.apps.custom_perm.models import BaseModel, BaseDeviceNodeModel
from backend.apps.device_models.models import EnvironmentMonitor
from backend.apps.projects.models import OrgTree


class EnvironmentMonitorNode(BaseDeviceNodeModel):
    """
    环境系统 - 树结构
    """

    org = models.ForeignKey(
        OrgTree,
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    environment_monitor = models.ForeignKey(
        EnvironmentMonitor,
        related_name='environment_monitor_nodes',
        on_delete=models.CASCADE,
        verbose_name='环境系统设备',
        help_text='环境系统设备',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '环境系统-树结构'
        verbose_name_plural = verbose_name


class EnvironmentDevice(models.Model):
    """
    环境系统应用设备
    """
    environment_monitor = models.ForeignKey(
        EnvironmentMonitor,
        related_name='environment_devices',
        on_delete=models.CASCADE,
        verbose_name='环境系统设备',
        help_text='环境系统设备'
    )
    node = models.OneToOneField(
        EnvironmentMonitorNode,
        related_name='node_environment_device',
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
        verbose_name = '环境系统应用设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.node.name


class EnvDistribution(BaseModel):
    """
    环境系统 - 分布图
    """

    org = models.ForeignKey(
        OrgTree,
        related_name='org_env_distributions',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
    )
    name = models.CharField(
        verbose_name='名称',
        help_text='名称',
        max_length=100,
    )
    image = models.TextField(
        verbose_name='分布图',
        help_text='分布图',
        null=True,
        blank=True,
    )
    is_polling = models.BooleanField(
        default=False,
        verbose_name='是否开启设备轮训',
        help_text='是否开启设备轮训'
    )
    dmap_env_devices = models.JSONField(
        verbose_name='分布图设备',
        help_text='分布图设备',
        null=True,
        blank=True,
    )
    alternative_images = models.JSONField(
        verbose_name='分布图images',
        help_text='分布图images',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '环境系统-分布图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
