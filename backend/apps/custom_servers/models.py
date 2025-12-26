from django.db import models


class Domain(models.Model):

    class Meta:
        verbose_name = '统一身份认证服务域名'
        verbose_name_plural = verbose_name

    name = models.CharField(
        verbose_name='名称',
        help_text='api域名:端口号 或 api域名',
        max_length=200,
        unique=True
    )
    title = models.CharField(
        verbose_name='网站名称',
        max_length=50,
        default=None,
        null=True,
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='logo',
        upload_to='serve_logos',
        help_text='logo',
        null=True,
        blank=True,
    )
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_time = models.DateTimeField(auto_now_add=True)
    we_svc_app_id = models.CharField(
        verbose_name='微信服务号 APP ID',
        max_length=20,
        default=None,
        null=True,
        blank=True,
    )
    we_svc_app_secret = models.CharField(
        verbose_name='微信服务号 APP SECRET',
        max_length=32,
        default=None,
        null=True,
        blank=True,
    )
    we_svc_id = models.CharField(
        verbose_name='微信服务号 原始ID',
        max_length=18,
        default=None,
        null=True,
        blank=True,
    )
    we_svc_qrcode = models.CharField(
        verbose_name='微信服务号 二维码',
        max_length=200,
        default=None,
        null=True,
        blank=True,
    )
    we_svc_alarm_tpl_id = models.CharField(
        verbose_name='告警消息模板ID',
        max_length=50,
        default=None,
        null=True,
        blank=True,
    )
    weapp_app_id = models.CharField(
        verbose_name='微信小程序 APP ID',
        max_length=20,
        default=None,
        null=True,
        blank=True,
    )
    weapp_app_secret = models.CharField(
        verbose_name='微信小程序 APP SECRET',
        max_length=32,
        default=None,
        null=True,
        blank=True,
    )
    weapp_id = models.CharField(
        verbose_name='微信小程序 原始ID',
        max_length=18,
        default=None,
        null=True,
        blank=True,
    )
    we_mch_id = models.CharField(
        verbose_name='微信商户号ID',
        help_text='微信商户号ID',
        max_length=32,
        default=None,
        null=True,
        blank=True,
    )
    we_mch_serial_no = models.CharField(
        verbose_name='微信商户API证书序列号',
        help_text='微信商户API证书序列号',
        max_length=64,
        default=None,
        null=True,
        blank=True,
    )
    wx_pay_fee = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        verbose_name="手续费(元)",
        help_text='手续费(元)',
        default=0.006
    )

    @classmethod
    def get_we_svc(cls, we_svc_id):
        """
        获取微信服务号的 we_svc_app_id 和 we_svc_app_secret
        :param we_svc_id: 微信服务号原始ID
        :return: (we_svc_app_id, we_svc_app_secret) 或 None
        """
        qs = cls.objects.filter(we_svc_id=we_svc_id)
        if not qs.exists():
            return None, None
        obj = qs.first()
        if not obj.we_svc_app_id:
            return None, None
        if qs.exists() and qs.first().we_svc_app_id:
            return obj.we_svc_app_id, obj.we_svc_app_secret
        return None, None

    def __str__(self):
        return self.name



class ClientDomain(models.Model):

    class Meta:
        verbose_name = '客户端域名'
        verbose_name_plural = verbose_name

    domain = models.ForeignKey(
        Domain,
        help_text='统一身份认证服务域名',
        verbose_name='统一身份认证服务域名',
        related_name='client_domains',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='名称',
        help_text='api域名:端口号 或 api域名',
        max_length=200,
        unique=True
    )
    mobile = models.CharField(
        verbose_name='移动端域名',
        max_length=200,
        default=None,
        null=True,
        blank=True,
    )
    title = models.CharField(
        verbose_name='网站名称',
        max_length=50,
        default=None,
        null=True,
        blank=True,
    )
    logo = models.ImageField(
        verbose_name='logo',
        upload_to='serve_logos',
        help_text='logo',
        null=True,
        blank=True,
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )