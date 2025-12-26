from django.db import models
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from backend.apps.projects.models import OrgTree
from backend.apps.device_models.models import ElectricMeter


class StatisticDimension(models.Model):
    """
    能耗统计 - 统计维度表
    """
    # 设备分类
    ENERGY_TYPE_CHOICES = (
        ('water', '水'),
        ('electric', '电'),
        ('gas', '气'),
        ('heating', '暖'),
    )

    org = models.ForeignKey(
        OrgTree,
        related_name='org_stat_dimensions',
        on_delete=models.CASCADE,
        verbose_name='组织',
        help_text='组织',
        null=True,
        blank=True
    )
    name = models.CharField(
        verbose_name='统计维度名称',
        help_text='统计维度名称',
        max_length=20,
        blank=True
    )
    energy_type = models.CharField(
        verbose_name='设备分类',
        help_text='设备分类',
        choices=ENERGY_TYPE_CHOICES,
        max_length=10,
    )
    ordering = models.IntegerField(
        verbose_name='排序',
        help_text='排序',
        db_index=True,
        default=0
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
        verbose_name = '能耗统计维度表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DimensionNode(MPTTModel):
    """
    能耗统计 -统计维度节点表
    """
    stat_dimension = models.ForeignKey(
        StatisticDimension,
        related_name='stat_dimension_nodes',
        on_delete=models.CASCADE,
        verbose_name='统计维度',
        help_text='统计维度',
        null=True,
        blank=True
    )
    name = models.CharField(
        verbose_name='节点名称',
        help_text='节点名称',
        max_length=60,
        blank=True
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='父节点',
        help_text='父节点',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
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
        verbose_name = '统计维度节点表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ElectricMeterNode(models.Model):
    """
    能耗统计- 数据源 节点电表配置
    """

    R_TYPE_CHOICES = (
        ('+', '加'),
        ('-', '减')
    )

    node = models.ForeignKey(
        DimensionNode,
        related_name='node_electric_meters',
        on_delete=models.CASCADE,
        verbose_name='所属节点',
        help_text='所属节点'
    )
    electric_meter = models.ForeignKey(
        ElectricMeter,
        related_name='electric_meter_nodes',
        on_delete=models.CASCADE,
        verbose_name='电表',
        help_text='电表'
    )
    relation_type = models.CharField(
        verbose_name='运算关系‌',
        help_text='运算关系‌',
        choices=R_TYPE_CHOICES,
        db_index=True,
        max_length=10,
    )

    class Meta:
        verbose_name = '维度节点电表配置'
        verbose_name_plural = verbose_name

