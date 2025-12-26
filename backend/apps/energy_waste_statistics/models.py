from django.db import models
from django.utils import timezone
from backend.apps.projects.models import OrgTree
from backend.apps.device_models.models import ElectricMeter


class EnergyWasteGroup(models.Model):
    """
    能耗浪费 -分组表
    """
    org = models.ForeignKey(
        OrgTree,
        related_name='org_ew_groups',
        on_delete=models.CASCADE,
        verbose_name='组织',
        help_text='组织',
    )
    name = models.CharField(
        verbose_name='分组名称',
        help_text='分组名称',
        max_length=100
    )
    ordering = models.PositiveBigIntegerField(
        verbose_name='排序',
        help_text='排序',
        db_index=True,
        default=0
    )
    working_time_cfg = models.JSONField(
        verbose_name='工作时间信息',
        help_text='工作时间信息',
        null=True,
        blank=True,
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = ' 能耗浪费分组表'
        verbose_name_plural = verbose_name
        unique_together = ('org', 'name')

    def __str__(self):
        return self.name


class EnergyWasteDevice(models.Model):
    """
    能耗浪费 - 设备
    """
    org = models.ForeignKey(
        OrgTree,
        related_name='org_ew_devices',
        on_delete=models.CASCADE,
        verbose_name='组织',
        help_text='组织',
    )
    group = models.ForeignKey(
        EnergyWasteGroup,
        related_name='group_ew_devices',
        on_delete=models.SET_NULL,
        verbose_name='所属分组',
        help_text='所属分组',
        null=True,
        blank=True
    )
    ordering = models.PositiveBigIntegerField(
        verbose_name='分组排序',
        help_text='分组排序',
        db_index=True,
        default=0
    )
    electric_meter = models.ForeignKey(
        ElectricMeter,
        on_delete=models.CASCADE,
        verbose_name='电表',
        help_text='电表'
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '能耗浪费设备'
        verbose_name_plural = verbose_name
        unique_together = ('org', 'electric_meter')


class EnergyWasteDailyCfg(models.Model):
    """
    分组能耗浪费统计每日配置表
    """
    group = models.ForeignKey(
        EnergyWasteGroup,
        related_name='group_ew_cfgs',
        on_delete=models.CASCADE,
        verbose_name='所属分组',
        help_text='所属分组'
    )
    working_time_cfg = models.JSONField(
        verbose_name='工作时间信息',
        help_text='工作时间信息'
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '分组能耗浪费统计每日配置表'
        verbose_name_plural = verbose_name


class EnergyWasteDailyData(models.Model):
    """
    分组能耗浪费每日统计数据
    """

    group = models.ForeignKey(
        EnergyWasteGroup,
        related_name='group_ew_datas',
        on_delete=models.CASCADE,
        verbose_name='所属分组',
        help_text='所属分组'
    )
    ew_daily_cfg = models.ForeignKey(
        EnergyWasteDailyCfg,
        on_delete=models.SET_NULL,
        verbose_name='当日统计配置',
        help_text='当日统计配置',
        null=True,
        blank=True
    )
    numb = models.FloatField(
        verbose_name="浪费电量",
        help_text='浪费电量',
        null=True,
        blank=True
    )
    devices_data = models.JSONField(
        verbose_name='设备统计明细',
        help_text='设备统计明细',
        null=True,
        blank=True
    )
    statistic_date = models.DateField(
        verbose_name='统计日期',
        help_text='统计日期',
        db_index=True
    )

    class Meta:
        verbose_name = '能耗浪费统计数据'
        verbose_name_plural = verbose_name
        unique_together = ('group', 'statistic_date')
