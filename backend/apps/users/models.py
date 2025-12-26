import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from backend.apps.common.fields import CharNullField
from backend.apps.areas.models import Area
from backend.apps.projects.models import Projects


class User(AbstractUser):

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    uuid = models.UUIDField(
        verbose_name='UUID',
        help_text='跨系统用户关联的唯一标识',
        unique=True,        # 重新启用唯一约束
        default=uuid.uuid4, # 恢复默认值
        null=False,         # 禁止空值
        blank=False,        # 禁止表单空白
    )
    nickname = models.CharField(
        verbose_name='中文名',
        help_text='中文名',
        max_length=50,
        default='匿名',
    )
    mobile = CharNullField(
        verbose_name='手机号',
        help_text='手机号',
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )
    email = CharNullField(
        verbose_name='邮箱',
        help_text='邮箱',
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )
    last_updated = models.DateTimeField(
        verbose_name='最后更新时间',
        help_text='记录用户信息最后修改时间',
        null=True,
        blank=True,
    )
    avatar = models.TextField(
        verbose_name="用户头像",
        help_text="用户头像",
        null=True,
        blank=True,
    )
    remark = models.TextField(
        verbose_name="备注",
        help_text="备注",
        null=True,
        blank=True,
    )
    address = models.CharField(
        verbose_name="地址",
        help_text="地址",
        max_length=150,
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        'self',
        related_name='created_users',
        verbose_name="创建者",
        help_text="创建者",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_sys = models.BooleanField(
        verbose_name='是否系统内用户',
        help_text="是否系统内用户",
        default=True,
    )
    is_deleted = models.BooleanField(
        verbose_name='是否已删除',
        help_text="是否已删除",
        default=False,
    )
    token = models.CharField(
        help_text="机器用户可基于token访问API",
        max_length=20,
        null=True,
        blank=True
    )
    default_project = models.ForeignKey(
        Projects,
        verbose_name='默认项目',
        help_text="默认项目",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    default_style = models.TextField(
        verbose_name='默认样式',
        help_text='默认样式',
        null=True,
        blank=True
    )
    default_city = models.ForeignKey(
        to=Area,
        help_text="默认城市",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_userinfo(self):
        return {
            "username": self.username,
            "nickname": self.nickname,
            "mobile": self.mobile
        }

    def __str__(self):
        return self.nickname

    @property
    def masked_mobile(self):
        """
        返回脱敏后的手机号，格式如：189****6586
        """
        if not self.mobile:
            return None
        
        mobile = str(self.mobile)
        if len(mobile) < 7:
            return mobile  # 如果手机号长度不足7位，直接返回原值
        
        # 保留前3位和后4位，中间用*替换
        return mobile[:3] + '****' + mobile[-4:]

    @property
    def masked_email(self):
        """
        返回脱敏后的邮箱，格式如：abc****@example.com
        """
        if not self.email:
            return None
        
        email = str(self.email)
        if '@' not in email:
            return email  # 如果不是有效的邮箱格式，直接返回原值
        
        # 分割用户名和域名
        username, domain = email.split('@', 1)
        
        if len(username) <= 2:
            # 如果用户名长度小于等于2，只显示第一个字符
            masked_username = username[0] + '*' * (len(username) - 1)
        else:
            # 保留前2位和后1位，中间用*替换
            masked_username = username[:2] + '*' * (len(username) - 3) + username[-1]
        
        return f"{masked_username}@{domain}"
