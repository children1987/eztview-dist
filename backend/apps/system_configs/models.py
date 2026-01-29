from django.db import models

from backend.apps.common.models import BaseModel


class SystemConfig(BaseModel):
    """
    系统级配置，用于简单的 key-value 存储。
    例如：模块裁剪配置 module_trim 等。
    """

    key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="配置键",
        help_text="配置键，例如 module_trim",
    )
    value = models.TextField(
        verbose_name="配置值",
        help_text="配置值内容，JSON 或文本",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "系统配置"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:  # pragma: no cover
        return self.key


