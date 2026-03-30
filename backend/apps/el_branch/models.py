from django.db import models
from django.utils import timezone

from backend.apps.custom_perm.models import BaseDeviceNodeModel
from backend.apps.device_models.models import ElMonitorInstrument
# 注意：使用字符串引用避免循环依赖 (el_branch <-> projects)
# projects 导入 el_branch.BranchTreeNode，所以这里不能直接导入 OrgTree


class BranchTreeNode(BaseDeviceNodeModel):
    """
    回路配置 - 树结构
    """
    org = models.ForeignKey(
        'projects.OrgTree',  # 使用字符串引用避免循环依赖
        related_name='org_branch_nodes',
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织',
        null=True,
        blank=True
    )
    el_monitor = models.ForeignKey(
        ElMonitorInstrument,
        related_name='el_instrument_nodes',
        on_delete=models.CASCADE,
        verbose_name='电气监测仪表',
        help_text='电气监测仪表',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '回路配置-树结构'
        verbose_name_plural = verbose_name


class ElInstrument(models.Model):
    """
    回路配置-电气仪表
    """
    el_monitor = models.ForeignKey(
        ElMonitorInstrument,
        related_name='el_instruments',
        on_delete=models.CASCADE,
        verbose_name='电气监测仪表',
        help_text='电气监测仪表'
    )
    node = models.OneToOneField(
        BranchTreeNode,
        related_name='node_el_instrument',
        on_delete=models.CASCADE,
        verbose_name='分组',
        help_text='分组',
        null=True,
        blank=True,
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )

    class Meta:
        verbose_name = '回路配置-电气仪表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.node.name


class DBTDataManager(object):

    @staticmethod
    def clear_data(org, remove_app=False):
        """
        清除组织在该应用下所有的数据
        :param org:
        :param remove_app: 是否移除该app
        :return:
        """
        # 删除分组其余数据级联删除
        BranchTreeNode.objects.filter(org=org).delete()
