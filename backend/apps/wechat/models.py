from django.db import models

from backend.apps.custom_servers.models import Domain

# 注意：使用字符串引用避免循环依赖
# users 导入 wechat，所以这里不能直接导入 User，使用字符串引用 'users.User'


class WechatUser(models.Model):

    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        on_delete=models.CASCADE
    )

    service_account_openid = models.CharField(
        max_length=64,
        verbose_name="微信服务号openid",
        default=None,
        null=True,
        blank=True,
    )

    domain = models.ForeignKey(
        Domain,
        help_text='服务域名',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None
    )

    unionid = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="微信开放平台unionid",
    )

    class Meta:
        unique_together = (
            ('user', 'domain', ),
        )


class WeappUser(models.Model):

    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        on_delete=models.CASCADE
    )

    openid = models.CharField(
        max_length=64,
        verbose_name="微信小程序openid",
    )

    domain = models.ForeignKey(
        Domain,
        help_text='服务域名',
        on_delete=models.CASCADE,
        default=None
    )

    class Meta:
        unique_together = (
            ('user', 'domain', ),
        )
