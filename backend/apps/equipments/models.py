from django.db import models
from django.utils import timezone
from backend.apps.custom_perm.models import BaseModel
from backend.apps.device_models.biz.device_model_manage import DeviceModelMixin
from backend.apps.projects.models import Projects, ProjectMembers, OrgTree

# 注意：使用字符串引用避免循环依赖
# projects 导入 equipments，而 projects 使用字符串引用 'users.User'
# 为了保持一致性和避免潜在问题，这里也使用字符串引用 'users.User'


class EZtProjects(models.Model):
    """
    Ezt项目
    """
    name = models.CharField(
        verbose_name='项目名称',
        help_text="项目名称",
        max_length=100,
        default='尚未命名',
    )
    desc = models.TextField(
        verbose_name='项目描述',
        help_text="项目描述",
        null=True,
        blank=True,
    )
    project_key = models.CharField(
        unique=True,
        verbose_name=' Ezt项目project_key',
        help_text='Ezt项目project_key 通常以"PR_"开头，如"PR_xxxxxxxxxx',
        max_length=30
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
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DeviceCategory(models.Model):
    """
    设备类型表
    """

    # 设备的节点类型
    DEVICE_NODE_TYPE = (
        ('DD', '直连设备'),
        ('CG', '网关'),
        ('SD', '子设备'),
    )

    project = models.ForeignKey(
        Projects,
        related_name='device_category',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    ezt_project = models.ForeignKey(
        EZtProjects,
        on_delete=models.CASCADE,
        verbose_name='EZt项目',
        help_text='EZt项目'
    )
    category_id = models.CharField(
        verbose_name='EZt设备类型ID',
        help_text='EZt设备类型ID',
        max_length=50,
        null=True,
        blank=True,
    )
    key = models.CharField(
        verbose_name='EZt设备类型唯一标识',
        help_text='EZt设备类型唯一标识',
        max_length=16,
        unique=True,
        null=True,
        blank=True,
    )
    category_name = models.CharField(
        verbose_name='EZt设备类型名称',
        help_text='EZt设备类型名称',
        max_length=30,
        null=True,
        blank=True
    )
    desc = models.TextField(
        verbose_name='设备类型描述',
        help_text='设备类型描述',
        null=True,
        blank=True,
    )
    node_type = models.CharField(
        verbose_name='设备接入类型',
        help_text='设备接入类型',
        choices=DEVICE_NODE_TYPE,
        max_length=20,
        null=True,
        blank=True
    )
    online_delay_time = models.IntegerField(
        verbose_name='设备在线延迟时间',
        help_text='设备在线延迟时间',
        default=300,
    )
    scene_action = models.BooleanField(
        verbose_name='是否参与场景动作',
        help_text="是否参与场景动作",
        default=True,
    )
    scene_condition = models.BooleanField(
        verbose_name='是否参与场景条件',
        help_text="是否参与场景条件",
        default=True,
    )
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="创建人",
        help_text="创建人",
        on_delete=models.SET_NULL,
        null=True
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    is_invalid = models.BooleanField(
        default=False,
        verbose_name='是否已失效',
        help_text='是否已失效'
    )

    class Meta:
        verbose_name = '设备类型表'
        verbose_name_plural = verbose_name


class CategoryModeMapping(models.Model):
    """
    设备类型关联模型映射表
    """
    DEVICE_TYPE_MAP_ = DeviceModelMixin.MODEL_NAME_CHOICES

    DEVICE_TYPE_MAP = dict(DEVICE_TYPE_MAP_)

    category = models.ForeignKey(
        DeviceCategory,
        related_name='device_types',
        verbose_name="设备类型",
        help_text='设备类型',
        on_delete=models.CASCADE,
    )
    device_type = models.CharField(
        verbose_name='MCP设备模型',
        help_text='MCP设备模型',
        choices=DEVICE_TYPE_MAP_,
        max_length=30
    )
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="创建人",
        help_text="创建人",
        on_delete=models.SET_NULL,
        null=True
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )

    class Meta:
        verbose_name = '设备类型关联模型映射表'
        verbose_name_plural = verbose_name


class DeviceGroups(models.Model):
    """
    设备组
    """
    project = models.ForeignKey(
        Projects,
        related_name='project_device_groups',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='设备组名称',
        help_text="设备组名称",
        max_length=100,
    )
    desc = models.TextField(
        verbose_name='设备分组描述信息',
        help_text='设备分组描述信息',
        null=True,
        blank=True
    )
    created_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="创建时间",
        help_text="创建时间"
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="更新时间"
    )

    class Meta:
        verbose_name = '设备组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    设备
    """

    # 告警状态
    STATE_CHOICES = (
        ('normal', '正常'),
        ('pending', '告警待定'),
        ('alerting', '告警'),
    )

    project = models.ForeignKey(
        Projects,
        related_name='project_devices',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    orgs = models.ManyToManyField(
        OrgTree,
        related_name='org_devices',
        verbose_name='组织',
        help_text='组织'
    )
    category = models.ForeignKey(
        DeviceCategory,
        related_name='category_devices',
        verbose_name="设备类型",
        help_text='设备类型',
        on_delete=models.CASCADE,
    )
    belong_unit = models.CharField(
        verbose_name='EZt设备所属分组',
        help_text='EZt设备所属分组',
        max_length=100,
        null=True,
        blank=True,
    )
    device_group = models.ForeignKey(
        to=DeviceGroups,
        related_name='group_devices',
        verbose_name='所属设备分组',
        help_text='所属设备分组',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    com_gateway = models.CharField(
        verbose_name='网关唯一标识',
        help_text='网关唯一标识',
        max_length=100,
        null=True,
        blank=True,
    )
    alarm_status = models.CharField(
        verbose_name='告警状态',
        help_text='告警状态',
        max_length=20,
        choices=STATE_CHOICES,
        default='normal'
    )
    username = models.CharField(
        verbose_name='设别唯一标识',
        help_text='设别唯一标识',
        max_length=100,
        unique=True
    )
    name = models.CharField(
        verbose_name='设备名称',
        help_text="设备名称",
        max_length=100,
    )
    desc = models.TextField(
        verbose_name='设备描述信息',
        help_text='设备描述信息',
        null=True,
        blank=True
    )
    location = models.CharField(
        verbose_name='设备安裝位置',
        help_text='设备安裝位置',
        max_length=100,
        null=True,
        blank=True,
    )
    addr = models.CharField(
        verbose_name='子设备标识符',
        help_text='子设备标识符',
        max_length=50,
        null=True,
        blank=True
    )
    serial_id = models.CharField(
        max_length=64,
        verbose_name='设备序列号',
        help_text='设备序列号, 在同一个设备类型下唯一',
        null=True,
        blank=True,
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name='是否在线',
        help_text='是否在线'
    )
    timestamp = models.DateTimeField(
        verbose_name="数据更新时间",
        help_text='数据更新时间',
        db_index=True,
        null=True,
        blank=True
    )
    last_offline_time = models.DateTimeField(
        verbose_name="最后离线时间",
        help_text="最后离线时间",
        null=True,
        blank=True
    )
    ordering = models.IntegerField(
        verbose_name='排序',
        help_text='排序',
        db_index=True,
        default=0
    )
    is_invalid = models.BooleanField(
        default=False,
        verbose_name='是否已失效',
        help_text='是否已失效'
    )
    created_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="创建时间",
        help_text="创建时间"
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="更新时间"
    )

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DeviceSyncRecord(models.Model):
    """
    设备同步记录
    """
    # 设备同步状态
    SYNC_STATE_CHOICES = (
        ('syncing', '同步中'),
        ('succeeded', '同步成功'),
        ('failed', '同步失败')
    )

    project = models.ForeignKey(
        Projects,
        related_name='device_sync_records',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    operator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="操作人",
        help_text="操作人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    state = models.CharField(
        verbose_name='同步状态',
        help_text='同步状态',
        choices=SYNC_STATE_CHOICES,
        max_length=20,
        default='syncing'
    )
    category_ids = models.TextField(
        verbose_name='同步设备类型ID',
        help_text='同步设备类型ID',
        default=''
    )
    remark = models.CharField(
        verbose_name='备注',
        help_text='备注',
        max_length=200,
        null=True,
        blank=True
    )
    device_count = models.IntegerField(
        verbose_name='设备总数量',
        help_text='设备总数量',
    )
    added_count = models.IntegerField(
        verbose_name='已添加数量',
        help_text='已添加数量',
    )
    sync_count = models.IntegerField(
        verbose_name='实际同步数量',
        help_text='实际同步数量',
        default=0
    )
    operate_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="操作时间",
        help_text="操作时间"
    )
    finish_time = models.DateTimeField(
        verbose_name="完成时间",
        help_text="完成时间",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备同步记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project.name + '同步记录'


class DeviceControlLogging(models.Model):
    """
    设备操控日志
    """
    app_key = models.CharField(
        verbose_name='应用菜单Key',
        help_text='应用菜单Key',
        max_length=100
    )
    devices = models.ManyToManyField(
        Device,
        related_name='device_control_logs',
        verbose_name='操作设备',
        help_text='操作设备'
    )
    operation_name = models.CharField(
        verbose_name='操作名称',
        help_text='操作名称',
        max_length=200,
        default=''
    )
    set_msg = models.JSONField(
        verbose_name='控制指令信息',
        help_text='控制指令信息',
    )
    operation_time = models.DateTimeField(
        verbose_name='操作时间',
        help_text='执行时间',
        default=timezone.now
    )
    operator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name='操作人',
        on_delete=models.SET_NULL,
        related_name='user_control_logs',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备操控日志'
        verbose_name_plural = verbose_name
