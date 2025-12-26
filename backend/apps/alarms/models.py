from django.db import models

from django.utils import timezone

from backend.apps.equipments.models import Device


class DeviceAlarmLogs(models.Model):
    """
    设备告警日志
    """
    ALARM_DEGREE_MAP = (
        ('10', '紧急'),
        ('20', '重要'),
        ('30', '普通'),
    )
    # 告警状态
    STATE_CHOICES = (
        ('normal', '正常'),
        ('pending', '告警待定'),
        ('alerting', '告警'),
    )
    STATE_MAP = dict(STATE_CHOICES)

    device = models.ForeignKey(
        Device,
        related_name='device_alarm_logs',
        verbose_name='设备',
        on_delete=models.CASCADE
    )
    degree = models.CharField(
        verbose_name='告警级别',
        help_text='告警级别',
        max_length=10,
        choices=ALARM_DEGREE_MAP,
    )
    alarm_status = models.CharField(
        verbose_name='告警状态',
        help_text='告警状态',
        max_length=20,
        choices=STATE_CHOICES,
    )
    alarm_type = models.CharField(
        verbose_name='告警类型',
        help_text='告警类型',
        default='',
        db_index=True
    )
    is_restored = models.BooleanField(
        verbose_name='是否已恢复',
        help_text='是否已恢复',
        default=False,
        db_index=True
    )
    alarm_rule_id = models.CharField(
        verbose_name='EZt告警规则ID',
        help_text='EZt告警规则ID',
        max_length=50,
        db_index=True
    )
    alarm_rule_name = models.CharField(
        verbose_name='EZt告警规则名称',
        help_text='EZt告警规则名称',
        max_length=100,

    )
    alarm_detail = models.JSONField(
        verbose_name='告警详情',
        help_text='告警详情',
        null=True,
        blank=True,
    )
    alarm_time = models.DateTimeField(
        verbose_name="告警规则状态改变时间",
        help_text="告警规则状态改变时间",
    )
    created_time = models.DateTimeField(
        verbose_name="创建时间",
        help_text="创建时间",
        default=timezone.now,
    )

    class Meta:
        verbose_name = '设备告警日志'
        verbose_name_plural = verbose_name
