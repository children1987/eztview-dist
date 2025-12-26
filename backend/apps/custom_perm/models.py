from django.contrib.auth.models import Permission, Group
from django.db import models
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
# 注意：使用字符串引用避免循环依赖 (custom_perm <-> equipments)
# equipments 导入 custom_perm.BaseModel，所以这里不能直接导入 Device


class BaseModel(models.Model):
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
        abstract = True


class BaseDeviceNodeModel(MPTTModel):
    """
    设备节点抽象模
    """
    NODE_TYPE_CHOICES = (
        ("group", "分组"),
        ("device", "设备"),
    )

    name = models.CharField(
        verbose_name='节点名称',
        help_text='节点名称',
        max_length=60,
        blank=True,
        null=True
    )
    node_type = models.CharField(
        verbose_name='节点类型',
        help_text='节点类型',
        choices=NODE_TYPE_CHOICES,
        db_index=True,
        max_length=10,
        default='group'
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='父节点',
        help_text='父节点',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    device = models.ForeignKey(
        'equipments.Device',  # 使用字符串引用避免循环依赖
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备',
        null=True,
        blank=True
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
        abstract = True

    def __str__(self):
        return self.name or self.device.name

    def is_leaf_node(self):
        """
        判断是否是叶子节点
        """
        if self.node_type == 'device':
            return True
        is_leaf = not self.get_descendant_count()
        if not is_leaf:
            return not self._meta.model.objects.filter(parent=self).exists()
        return is_leaf

    def is_leaf_group(self):
        """
        判断文件夹否是叶子节点
        """
        if self.node_type == 'group':
            return not self.get_children().filter(node_type='group').exists()
        return False


class PermissionManage(models.Model):
    """
    权限管理模型
    """
    category = models.CharField(verbose_name='菜单大类', max_length=50)
    permissions = models.ManyToManyField(
        Permission, verbose_name='权限',
        related_name='manage_permissions')

    class Meta:
        verbose_name = '权限管理类'
        verbose_name_plural = verbose_name


class GroupDetail(models.Model):
    """
   角色明细
   """
    group = models.OneToOneField(
        Group,
        verbose_name='角色',
        related_name='group_detail',
        on_delete=models.CASCADE
    )
    description = models.TextField(
        verbose_name='角色描述',
        help_text='角色描述',
        null=True,
        blank=True
    )
    remark = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = '角色明细表'
        verbose_name_plural = verbose_name


class GroupManagement(models.Model):
    """
   角色管理
   """
    group = models.ForeignKey(
        Group,
        verbose_name='角色',
        on_delete=models.CASCADE
    )

    manage_group = models.ForeignKey(
        Group,
        verbose_name='管理角色',
        related_name='manage_groups',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name
