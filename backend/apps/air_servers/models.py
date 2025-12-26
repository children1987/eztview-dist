from django.db import models
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from backend.apps.device_models.models import AirConditioner, PersonnelSensor, \
    SpaceTightSensor
from backend.apps.projects.models import OrgTree


class AirCondGroup(MPTTModel):
    """
    中央空调 - 树结构
    """

    org = models.ForeignKey(
        OrgTree,
        related_name='org_air_groups',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    name = models.CharField(
        verbose_name='节点名称',
        help_text='节点名称',
        max_length=20,
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
        verbose_name = '中央空调分组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def is_leaf_node(self):
        """
        判断是否是叶子节点
        """
        is_leaf = not self.get_descendant_count()
        if not is_leaf:
            return not self._meta.model.objects.filter(parent=self).exists()
        return is_leaf



class CentralAirConditioner(models.Model):
    """
    中央空调
    """
    air_cond = models.OneToOneField(
        AirConditioner,
        related_name='central_air_cond',
        on_delete=models.CASCADE,
        verbose_name='空调',
        help_text='空调'
    )
    group = models.ForeignKey(
        AirCondGroup,
        related_name='group_air_conds',
        on_delete=models.CASCADE,
        verbose_name='分组',
        help_text='分组',
        null=True,
        blank=True,
    )
    is_auto_off = models.BooleanField(
        default=False,
        verbose_name='是否启用无人自动关闭',
        help_text='是否启用无人自动关闭',
    )
    off_delay_minutes = models.IntegerField(
        verbose_name='无人自动关闭延时分钟数',
        help_text='无人自动关闭延时分钟数',
        null=True,
        blank=True,
    )
    order = models.IntegerField(
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
        verbose_name = '中央空调_空调设备'
        verbose_name_plural = verbose_name


class AirPersonnelSensor(models.Model):
    """
    中央空调_人体存在感应传感器
    """
    personnel_sensor = models.OneToOneField(
        PersonnelSensor,
        related_name='air_personnel_sensor',
        on_delete=models.CASCADE,
        verbose_name='人体存在传感器',
        help_text='人体存在传感器'
    )
    group = models.ForeignKey(
        AirCondGroup,
        related_name='group_personnel_sensors',
        on_delete=models.CASCADE,
        verbose_name='分组',
        help_text='分组',
        null=True,
        blank=True,
    )
    order = models.IntegerField(
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
        verbose_name = '中央空调_人体存在感应传感器'
        verbose_name_plural = verbose_name


class AirSpaceTightSensor(models.Model):
    """
    中央空调_门窗传感器
    """
    space_tight_sensor = models.OneToOneField(
        SpaceTightSensor,
        related_name='air_st_sensor',
        on_delete=models.CASCADE,
        verbose_name='门窗传感器',
        help_text='门窗传感器'
    )
    group = models.ForeignKey(
        AirCondGroup,
        related_name='group_space_tight_sensors',
        on_delete=models.CASCADE,
        verbose_name='分组',
        help_text='分组',
        null=True,
        blank=True,
    )
    order = models.IntegerField(
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
        verbose_name = '中央空调_门窗传感器'
        verbose_name_plural = verbose_name