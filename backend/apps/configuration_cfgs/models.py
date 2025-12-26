from django.db import models
from django.utils import timezone

from backend.apps.projects.models import OrgTree
# 注意：使用字符串引用避免循环依赖
# projects 使用字符串引用 'users.User'，为了保持一致，这里也使用字符串引用
from backend.apps.equipments.models import Device


class BaseVariable(models.Model):
    """
    全局变量基类
    """
    class Meta:
        abstract = True

    org = models.ForeignKey(
        OrgTree,
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织'
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="更新时间"
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="创建人",
        help_text="创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class DeviceAttrVariable(BaseVariable):
    """
    设备属性变量
    """

    class Meta:
        verbose_name = '属性变量'
        verbose_name_plural = verbose_name
        unique_together = ('org', 'key')
        ordering = ('-id',)

    name = models.CharField(
        max_length=100,
        verbose_name='名称',
        help_text='名称',
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name='设备',
        help_text='设备'
    )
    attr_key = models.CharField(
        max_length=64,
        verbose_name='设备属性key',
        help_text='设备属性key',
    )
    key = models.CharField(
        max_length=100,
        verbose_name='属性变量key',
        help_text='属性变量key, device.DU_xxx.attr_key',
    )

    def __str__(self):
        return self.name


class ApiVariable(BaseVariable):
    """
    API变量
    """

    class Meta:
        verbose_name = 'API变量'
        verbose_name_plural = verbose_name
        unique_together = ('org', 'key')
        ordering = ('-id',)

    name = models.CharField(
        max_length=100,
        verbose_name='名称',
        help_text='名称',
    )
    key = models.CharField(
        max_length=64,
        verbose_name='API变量key',
        help_text='API变量key, api.xxx',
    )
    url = models.TextField(
        verbose_name='url',
        help_text='url, https://www.api.xxx',
    )
    method = models.CharField(
        max_length=10,
        verbose_name='请求方式',
        help_text='请求方式GET, POST',
    )
    body = models.TextField(
        verbose_name='请求体',
        help_text="请求体, {'xxx': 12}",
        null=True,
        blank=True
    )
    remark = models.CharField(
        max_length=200,
        verbose_name='备注',
        help_text="备注",
        null=True,
        blank=True,
    )
    is_auto_polling = models.BooleanField(
        verbose_name='是否自动轮询',
        help_text="是否自动轮询",
        default=False
    )
    polling_cycle = models.PositiveIntegerField(
        verbose_name='轮询周期/秒',
        help_text="轮询周期/秒",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name



class FrontCustomVariable(BaseVariable):
    """
    自定义变量
    """

    DATA_TYPE_ = (
        ('N', '数值(Number)'),
        ('B', '开关量(Boolean)'),
        ('T', '文本(String)'),
        ('E', '枚举(Enum)'),
        ('O', '键值对(Object)'),
        ('L', '列表(List)'),
    )

    class Meta:
        verbose_name = '自定义变量'
        verbose_name_plural = verbose_name
        unique_together = ('org', 'key')
        ordering = ('-id',)

    name = models.CharField(
        max_length=100,
        verbose_name='名称',
        help_text='名称',
    )
    key = models.CharField(
        max_length=100,
        verbose_name='自定义变量key',
        help_text='自定义变量key, front.xxx',
    )
    data_type = models.CharField(
        verbose_name='数据类型',
        help_text='数据类型',
        choices=DATA_TYPE_,
        max_length=10,
    )
    data_specs = models.JSONField(
        verbose_name='属性约束',
        help_text='属性约束',
        null=True,
        blank=True,
    )
    unit = models.CharField(
        max_length=100,
        verbose_name='单位',
        help_text='单位',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name