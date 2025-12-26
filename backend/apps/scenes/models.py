from django.db import models
from django.utils import timezone
from backend.apps.projects.models import OrgTree
# 注意：使用字符串引用避免循环依赖
# projects 使用字符串引用 'users.User'，为了保持一致，这里也使用字符串引用


class SceneConfig(models.Model):
    """
    场景设置
    """

    name = models.CharField(
        verbose_name='场景名称',
        help_text='场景名称',
        max_length=100
    )
    description = models.TextField(
        verbose_name='场景描述',
        help_text='场景描述',
        null=True,
        blank=True
    )
    project_key = models.CharField(
        verbose_name=' Ezt项目project_key',
        help_text='Ezt项目project_key 通常以"PR_"开头，如"PR_xxxxxxxxxx',
        max_length=30
    )
    scene_id = models.IntegerField(
        verbose_name=' EztCloud场景ID',
        help_text='EztCloud场景ID',
    )
    org = models.ForeignKey(
        OrgTree,
        related_name='org_scenes',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='是否启用',
        default=True,
        help_text='是否启用'
    )
    cfg_info = models.JSONField(
        verbose_name='场景配置详情',
        help_text='场景配置详情',
        null=True,
        blank=True
    )
    scene_devices_data = models.JSONField(
        verbose_name='场景配置详情',
        help_text='场景配置详情',
        null=True,
        blank=True
    )
    trigger_type = models.CharField(
        verbose_name='触发类型',
        help_text='触发类型',
        max_length=100,
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name='创建人',
        on_delete=models.SET_NULL,
        help_text='创建人',
        null=True,
        blank=True
    )
    created_time = models.DateTimeField(
        verbose_name="创建时间",
        help_text="创建时间",
        default=timezone.now,
    )
    updated_time = models.DateTimeField(
        verbose_name="更新时间",
        help_text="更新时间",
        auto_now=True,
    )

    class Meta:
        verbose_name = '场景设置'
        verbose_name_plural = verbose_name

