import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, Group
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from backend.apps.areas.models import Area
from backend.apps.custom_perm.models import BaseModel
# 注意：使用字符串引用避免循环依赖 (projects <-> equipments)
# equipments 导入 projects.Projects, ProjectMembers, OrgTree，所以这里不能直接导入 EZtProjects
from backend.apps.el_branch.models import BranchTreeNode
# 注意：使用字符串引用避免循环依赖 (projects <-> users)
# users 导入 projects.Projects，所以这里不能直接导入 User，使用字符串引用 'users.User'


class Projects(BaseModel):
    """
    项目
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
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
    alarm_types = models.JSONField(
        verbose_name='告警类型配置',
        help_text='告警类型配置',
        null=True,
        blank=True,
    )
    ezt_project = models.ForeignKey(
        'equipments.EZtProjects',  # 使用字符串引用避免循环依赖
        on_delete=models.SET_NULL,
        verbose_name='Ezt项目',
        help_text='Ezt项目',
        null=True,
        blank=True
    )
    title = models.CharField(
        verbose_name='项目标题',
        help_text="项目标题",
        max_length=100,
        default='EZtCloud数据应用系统'
    )
    ordering = models.IntegerField(
        verbose_name='项目排序',
        help_text="对自己创建的项目排序",
        default=0,
    )
    remark = models.TextField(
        verbose_name='项目备注',
        help_text="项目备注",
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="创建人",
        help_text="创建人",
        on_delete=models.PROTECT,
        null=True
    )
    is_deleted = models.BooleanField(
        verbose_name='是否已删除',
        help_text="是否已删除",
        default=False,
    )
    created_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="创建时间",
        help_text="创建时间",
        db_index=True
    )

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        permissions = (
            ("view_project_cfg", "查看控制台"),
            ("view_project_app", "查看工作台")
        )

    def __str__(self):
        return self.name


class OrgTree(MPTTModel):
    """
    项目机构树
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    project = models.ForeignKey(
        Projects,
        related_name='project_orgs',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='机构名称',
        help_text="机构名称",
        max_length=50,
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='上级机构',
        help_text='上级机构',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    ordering = models.IntegerField(verbose_name='排序', default=0)
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="项目成员记录创建人",
        help_text="项目成员记录创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
    el_branch_node = models.ForeignKey(
        BranchTreeNode,
        on_delete=models.SET_NULL,
        verbose_name='配电回路默认节点',
        help_text='配电回路默认节点',
        null=True,
        blank=True
    )
    app_default_cfg = models.JSONField(
        verbose_name='组织应用默认配置',
        help_text='组织应用默认配置',
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='是否删除',
        help_text='是否删除'
    )

    class Meta:
        verbose_name = '组织机构'
        verbose_name_plural = verbose_name
        permissions = (
            ("org_device_manage", "组织设备管理"),
            ("view_org_overview", "查看组织概览"),
            ("change_org_overview", "操作组织概览"),
            ("add_org_user", "组织成员"),
        )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ProjectMembers(models.Model):
    """项目成员明细"""

    # 用户级别
    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        related_name='user_members',
        verbose_name="项目成员",
        help_text="项目成员",
        on_delete=models.CASCADE
    )
    orgs = models.ManyToManyField(
        OrgTree,
        verbose_name='所属机构',
        help_text='所属机构',
        related_name='org_members',
    )
    project = models.ForeignKey(
        Projects,
        related_name='project_members',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    desc = models.TextField(
        verbose_name='描述',
        help_text="描述",
        null=True,
        blank=True,
    )
    ordering = models.IntegerField(verbose_name='排序', default=0)
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="项目成员记录创建人",
        help_text="项目成员记录创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        verbose_name = '项目成员明细'
        verbose_name_plural = verbose_name
        unique_together = ('project', 'user')


class ProjectsAppMenus(BaseModel):
    """
    项目应用
    """
    # 默认项目应用
    PROJECT_DEFAULT_APP = {
        'warningGessage': '告警信息',
    }

    project = models.ForeignKey(
        Projects,
        related_name='project_app_menus',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    app_key = models.CharField(
        verbose_name='应用菜单Key',
        help_text='应用菜单Key',
        max_length=100,
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name='应用名称',
        help_text="应用名称",
        max_length=100,
        default='尚未命名',
    )
    desc = models.TextField(
        verbose_name='项目应用描述',
        help_text="项目应用描述",
        null=True,
        blank=True,
    )
    ordering = models.IntegerField(verbose_name='排序', default=0)
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="项目应用创建人",
        help_text="项目应用建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        verbose_name = '项目应用'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrgAppMenus(BaseModel):
    """
    组织应用
    """

    org = models.ForeignKey(
        OrgTree,
        related_name='org_app_menus',
        verbose_name="所属组织",
        help_text="所属组织",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='应用名称',
        help_text="应用名称",
        max_length=100,
        default='尚未命名',
    )
    desc = models.TextField(
        verbose_name='项目应用描述',
        help_text="项目应用描述",
        null=True,
        blank=True,
    )
    project_app = models.ForeignKey(
        ProjectsAppMenus,
        related_name='project_app_orgs',
        verbose_name="项目应用",
        help_text="项目应用",
        on_delete=models.CASCADE,
    )
    ordering = models.IntegerField(verbose_name='排序', default=0)
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="组织应用创建人",
        help_text="组织应用创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '组织应用'
        verbose_name_plural = verbose_name
        unique_together = ('org', 'project_app')

    def __str__(self):
        return self.org.name + '-' + self.project_app.name


class ProjectGroup(BaseModel):
    """
    项目角色
    """
    project = models.ForeignKey(
        Projects,
        related_name='project_groups',
        verbose_name="项目",
        help_text="项目",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="角色名称",
        help_text="角色名称",
        max_length=150,
    )
    desc = models.TextField(
        verbose_name='角色描述',
        help_text="角色描述",
        null=True,
        blank=True,
    )
    permissions = models.ManyToManyField(
        Permission,
        related_name='perm_project_groups',
        verbose_name='角色权限',
        help_text='角色权限',
        blank=True,
    )
    users = models.ManyToManyField(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name='角色成员',
        help_text='角色成员',
        related_name='user_project_groups',
    )
    ordering = models.IntegerField(verbose_name='排序', default=0)
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="创建人",
        help_text="创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "项目角色"
        verbose_name_plural = "项目角色"
        unique_together = ('project', 'name')

    def __str__(self):
        return self.name
