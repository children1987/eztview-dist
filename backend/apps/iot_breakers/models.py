from django.db import models
from django.utils import timezone
from backend.apps.custom_perm.models import BaseDeviceNodeModel
from backend.apps.device_models.models import IotBreaker
from backend.apps.projects.models import OrgTree


class IotBreakerTreeNode(BaseDeviceNodeModel):
    """
    物联网断路器 - 树结构
    """

    org = models.ForeignKey(
        OrgTree,
        related_name='org_iot_breakers',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    iot_breaker = models.ForeignKey(
        IotBreaker,
        related_name='iot_breaker_nodes',
        on_delete=models.CASCADE,
        verbose_name='物联网断路器',
        help_text='物联网断路器',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '物联网断路器-树结构'
        verbose_name_plural = verbose_name


class IotBreakerDevice(models.Model):
    """
    物联网断路器-断路器设备
    """
    iot_breaker = models.ForeignKey(
        IotBreaker,
        related_name='iot_breaker_device',
        on_delete=models.CASCADE,
        verbose_name='物联网断路器',
        help_text='物联网断路器'
    )
    node = models.OneToOneField(
        IotBreakerTreeNode,
        related_name='node_iot_breaker',
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
        verbose_name = '物联网断路器-断路器设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.node.name

