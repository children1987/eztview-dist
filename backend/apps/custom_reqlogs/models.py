from django.db import models

from backend.apps.projects.models import OrgTree, Projects
# 注意：使用字符串引用避免循环依赖
# projects 使用字符串引用 'users.User'，为了保持一致，这里也使用字符串引用


class CustomRequestLogs(models.Model):
    """
    请求日志
    """
    action_name = models.CharField(
        verbose_name='请求内容', default='', max_length=50, db_index=True)
    execution_time = models.CharField(
        verbose_name='耗时', max_length=50)
    timestamp = models.DateTimeField(verbose_name='请求时间')
    ip_address = models.GenericIPAddressField(verbose_name='客户端ip')
    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name='请求人',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    app_key = models.CharField(
        verbose_name='应用菜单Key',
        help_text='应用菜单Key',
        max_length=100,
        db_index=True,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        Projects,
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    org = models.ForeignKey(
        OrgTree,
        verbose_name='组织',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    request_method = models.CharField(verbose_name='请求方式', max_length=20)
    full_path = models.TextField(verbose_name='请求地址')
    query_params = models.TextField(verbose_name='请求参数')
    data = models.TextField(verbose_name='请求体')
    res_code = models.IntegerField(
        verbose_name='响应code',
        null=True,
        blank=True
    )
    res_data = models.TextField(
        verbose_name='返回数据',
        help_text='返回数据',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '请求操作日志'
        verbose_name_plural = verbose_name
