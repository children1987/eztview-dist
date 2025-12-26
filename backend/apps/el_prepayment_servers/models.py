
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from backend.apps.custom_servers.models import Domain
from backend.apps.device_models.models import PrepaidElectricMeter
from backend.apps.projects.models import OrgTree
# 注意：使用字符串引用避免循环依赖
# users 导入 projects.Projects，所以这里不能直接导入 User，使用字符串引用 'users.User'


class PrepaidElMeterGroup(MPTTModel):
    """
    预付费电表-分组
    """

    class Meta:
        verbose_name = '预付费电表-分组'
        verbose_name_plural = verbose_name

    org = models.ForeignKey(
        OrgTree,
        related_name='el_meter_groups',
        on_delete=models.CASCADE,
        verbose_name='组织',
        help_text='组织',
    )
    name = models.CharField(
        verbose_name='分组名称',
        help_text='分组名称',
        max_length=100
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
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )


class BasePriceCfg(models.Model):
    """
    电费配置基础字段
    """
    class Meta:
        abstract = True

    is_time_of_use = models.BooleanField(
        default=False,
        verbose_name='是否使用复费率电费',
        help_text='是否使用复费率电费'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        verbose_name="普通电价(元/度)",
        help_text='普通电价(元/度)',
        null=True,
        blank=True,
    )
    top_price = models.DecimalField(
        verbose_name="尖电价(元/度)",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=6
    )
    on_peak_price = models.DecimalField(
        verbose_name="峰电价(元/度)",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=6
    )
    flat_price = models.DecimalField(
        verbose_name="平电价(元/度)",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=6
    )
    valley_price = models.DecimalField(
        verbose_name="谷电价(元/度)",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=6
    )
    deep_valley_price = models.DecimalField(
        verbose_name="深谷电价(元/度)",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=6
    )


class OrgPriceCfg(BasePriceCfg):

    class Meta:
        verbose_name = '预付费系统-组织电价方案'
        verbose_name_plural = verbose_name

    org = models.ForeignKey(
        OrgTree,
        related_name='price_cfgs',
        on_delete=models.PROTECT,
        verbose_name='所属组织',
        help_text='所属组织'
    )
    name = models.CharField(
        verbose_name='名称',
        help_text="名称",
        max_length=50,
    )
    desc = models.TextField(
        verbose_name='描述信息',
        help_text='描述信息',
        null=True,
        blank=True
    )
    waring_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="预警金额(元)",
        help_text='预警金额(元)',
        null=True,
        blank=True
    )
    trip_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="可透支金额(元)",
        help_text='可透支金额(元)',
        null=True,
        blank=True
    )
    creator = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="创建人",
        help_text="创建人",
        on_delete=models.PROTECT,
        null=True
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="更新时间"
    )

    def __str__(self):
        return self.org.name


class PrepaidOrgCfg(models.Model):

    class Meta:
        verbose_name = '预付费系统-组织配置'
        verbose_name_plural = verbose_name

    org = models.OneToOneField(
        OrgTree,
        related_name='prepaid_cfg',
        on_delete=models.PROTECT,
        verbose_name='所属组织',
        help_text='所属组织'
    )
    recharge_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="租客累计充值收益金额(元)",
        help_text='租客累计充值收益金额(元)',
        default=0
    )
    sum_fee = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="总支付费率(元)",
        help_text='总支付费率(元)',
        default=0
    )
    withdrawn_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="已提现金额(元)",
        help_text='已提现金额(元)',
        default=0
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="更新时间"
    )

    def __str__(self):
        return self.org.name

    @property
    def available_cash(self):
        """
        获取剩余可提现金额
        """
        return self.recharge_amount - self.withdrawn_amount


class PrepaidElMeter(BasePriceCfg):

    class Meta:
        verbose_name = '预付费系统-电表'
        verbose_name_plural = verbose_name

    SURPLUS_STATE_ = (
        ('normal', '正常'),
        ('warming', '预警'),
        ('arrears', '欠费')
    )

    org = models.ForeignKey(
        OrgTree,
        on_delete=models.PROTECT,
        verbose_name='所属组织',
        help_text='所属组织'
    )
    prepaid_el_meter = models.OneToOneField(
        PrepaidElectricMeter,
        related_name='prepaid_el_device',
        on_delete=models.SET_NULL,
        verbose_name='预付费电表',
        help_text='预付费电表',
        null=True,
        blank=True
    )
    waring_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="预警金额(元)",
        help_text='预警金额(元)',
        null=True,
        blank=True
    )
    trip_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="可透支金额(元)",
        help_text='可透支金额(元)',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        PrepaidElMeterGroup,
        related_name='group_el_meters',
        on_delete=models.SET_NULL,
        verbose_name='所属分组',
        help_text='所属分组',
        null=True,
        blank=True
    )
    surplus = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        verbose_name="电费余额(元)",
        help_text='电费余额(元)',
        default=0
    )
    surplus_state = models.CharField(
        verbose_name="余额状态",
        help_text='余额状态',
        max_length=20,
        choices=SURPLUS_STATE_,
        default='normal'
    )
    settle_time = models.DateTimeField(
        verbose_name='余额结算时间',
        help_text='余额结算时间',
        null=True,
        blank=True
    )
    first_epi = models.FloatField(
        verbose_name='电表初始码值(度)',
        help_text='电表初始码值(度)',
        null=True,
        blank=True
    )
    used_el = models.FloatField(
        verbose_name='累计耗电量(度)',
        help_text='累计耗电量(度)',
        default=0
    )
    recharge_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="租客累计充值金额(元)",
        help_text='租客累计充值金额(元)',
        default=0
    )
    real_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="累计收益金额(元)",
        help_text='累计收益金额(元)',
        default=0
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )
    updated_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="更新时间"
    )
    del_device_key = models.CharField(
        verbose_name="设备key",
        help_text='设备key',
        max_length=20,
        null=True,
        blank=True
    )
    del_device_info = models.JSONField(
        verbose_name="删除时设备信息",
        help_text='删除时设备信息',
        null=True,
        blank=True
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='是否删除',
        help_text='是否删除'
    )

    def __str__(self):
        if not self.prepaid_el_meter:
            return self.del_device_key or '电表已删除'
        return self.prepaid_el_meter.device.name

    @staticmethod
    def get_surplus_state(surplus, waring_amount):
        if surplus < 0:
            return 'arrears'
        if waring_amount is None:
            return 'normal'
        elif 0 <= surplus <= waring_amount:
            return 'warming'
        return 'normal'


class TenantElMeter(models.Model):
    class Meta:
        verbose_name = '预付费系统-租客电表'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'el_meter')

    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="租客",
        help_text="租客",
        on_delete=models.PROTECT
    )
    el_meter = models.ForeignKey(
        PrepaidElMeter,
        on_delete=models.PROTECT,
        verbose_name='预付费电表',
        help_text='预付费电表'
    )
    created_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )


class RechargeOrder(models.Model):
    class Meta:
        ordering = ('-id',)
        verbose_name = '预付费系统-充值订单'
        verbose_name_plural = verbose_name

    TRADE_STATE_ = (
        ('PENDING', '待支付'),
        ('SUCCESS ', '支付成功'),
        ('REFUND', '转入退款'),
        ('NOTPAY', '未支付'),
        ('CLOSED', '已关闭'),
        ('REVOKED', '已撤销'),
        ('USERPAYING', '用户支付中'),
        ('PAYERROR', '支付失败'),
    )
    TRADE_STATE_MAP = dict(TRADE_STATE_)
    TRADE_TYPE_ = (
        ('JSAPI', '公众号、小程序'),
        ('NATIVE', 'Native'),
        ('APP', 'APP'),
        ('MICROPAY', '付款码支付'),
        ('MWEB', 'H5支付'),
        ('FACEPAY', '刷脸支付')
    )
    PAYMENT_TYPE_ = (
        ('wx', '微信支付'),
        ('zfb', '支付宝'),
        ('bank', '银行卡'),
    )

    out_trade_no = models.CharField(
        verbose_name="商户订单号",
        help_text='商户订单号',
        max_length=32,
        unique=True
    )
    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="充值用户",
        help_text="充值用户",
        on_delete=models.PROTECT
    )
    el_meter = models.ForeignKey(
        PrepaidElMeter,
        related_name='recharge_orders',
        on_delete=models.SET_NULL,
        verbose_name='预付费电表',
        help_text='预付费电表',
        null=True,
        blank=True
    )
    domain = models.ForeignKey(
        Domain,
        help_text='服务域名',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )
    trade_state = models.CharField(
        verbose_name="订单交易状态",
        help_text='订单交易状态',
        max_length=20,
        choices=TRADE_STATE_,
        default='PENDING',
        db_index=True
    )
    trade_type = models.CharField(
        verbose_name="交易类型",
        help_text='交易类型',
        max_length=20,
        choices=TRADE_TYPE_,
        null=True,
        blank=True
    )
    payment_type = models.CharField(
        verbose_name="支付方式",
        help_text='支付方式',
        max_length=20,
        choices=PAYMENT_TYPE_,
        default='wx'
    )
    pay_time = models.DateTimeField(
        verbose_name="支付时间",
        help_text='支付时间',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="充值金额(元)",
        help_text='充值金额(元)'
    )
    remark = models.CharField(
        max_length=200,
        verbose_name='订单备注',
        help_text='订单备注',
        null=True,
        blank=True
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        default=timezone.now
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )


class RechargeRecord(models.Model):
    class Meta:
        verbose_name = '预付费系统-充值记录'
        verbose_name_plural = verbose_name

    PAYMENT_TYPES = (
        ('wx', '微信支付'),
        ('off_line', '线下充值')
    )

    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="充值用户",
        help_text="充值用户",
        on_delete=models.PROTECT
    )
    el_meter = models.ForeignKey(
        PrepaidElMeter,
        related_name='recharge_records',
        on_delete=models.PROTECT,
        verbose_name='预付费电表',
        help_text='预付费电表'
    )
    order_id = models.CharField(
        verbose_name="订单编号",
        help_text='订单编号',
        max_length=100,
        unique=True
    )
    payment_type = models.CharField(
        verbose_name="充值方式",
        help_text='充值方式',
        max_length=20,
        choices=PAYMENT_TYPES
    )
    surplus = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        verbose_name="充值后余额(元)",
        help_text='充值后余额(元)'
    )
    amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="充值金额(元)",
        help_text='充值金额(元)'
    )
    real_amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="实际到账金额(元)",
        help_text='实际到账金额(元)',
        null=True,
        blank=True
    )
    fee = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="手续费(元)",
        help_text='手续费(元)',
        null=True,
        blank=True
    )
    prepay_id = models.CharField(
        verbose_name='支付单号',
        help_text='由支付渠道返回的支付单号',
        max_length=100,
        null=True,
        blank=True
    )
    is_revenue = models.BooleanField(
        default=True,
        verbose_name='是否计入收益',
        help_text='是否计入收益'
    )
    created_time = models.DateTimeField(
        verbose_name='充值时间',
        default=timezone.now
    )
    remark = models.CharField(
        max_length=200,
        verbose_name='备注',
        help_text='备注',
        null=True,
        blank=True
    )

    @property
    def start_surplus(self):
        """
        充值前余额
        """
        return round(self.surplus, 2) - self.amount


class MeterReadRecord(BasePriceCfg):
    class Meta:
        ordering = ('-id',)
        verbose_name = '预付费系统-抄表记录'
        verbose_name_plural = verbose_name

    el_meter = models.ForeignKey(
        PrepaidElMeter,
        on_delete=models.PROTECT,
        verbose_name='预付费电表',
        help_text='预付费电表'
    )
    device = models.ForeignKey(
        'equipments.Device',
        on_delete=models.SET_NULL,
        verbose_name='关联设备',
        help_text='关联设备',
        null=True,
        blank=True
    )
    start_epi = models.FloatField(
        verbose_name='抄表起始总码值(度)',
        help_text='抄表起始总码值(度)',
        null=True,
        blank=True
    )
    end_epi = models.FloatField(
        verbose_name='抄表截止总码值(度)',
        help_text='抄表截止总码值(度)',
        null=True,
        blank=True
    )
    used_el = models.FloatField(
        verbose_name='使用总电量(度)',
        help_text='使用总电量(度)',
    )
    top_epi = models.FloatField(
        verbose_name="尖电能码值(度)",
        help_text="尖电能码值(度)",
        null=True,
        blank=True
    )
    used_top_epi = models.FloatField(
        verbose_name="使用尖电能(度)",
        help_text="使用尖电能(度)",
        null=True,
        blank=True
    )
    on_peak_epi = models.FloatField(
        verbose_name="峰电能码值(度)",
        help_text="峰电能码值(度)",
        null=True,
        blank=True
    )
    used_on_peak_epi = models.FloatField(
        verbose_name="使用峰电能(度)",
        help_text="使用峰电能(度)",
        null=True,
        blank=True
    )
    flat_epi = models.FloatField(
        verbose_name="平电能码值(度)",
        help_text="平电能码值(度)",
        null=True,
        blank=True
    )
    used_flat_epi = models.FloatField(
        verbose_name="使用平电能(度)",
        help_text="使用平电能(度)",
        null=True,
        blank=True
    )
    valley_epi = models.FloatField(
        verbose_name="谷电能码值(度)",
        help_text="谷电能码值(度)",
        null=True,
        blank=True
    )
    used_valley_epi = models.FloatField(
        verbose_name="使用谷电能(度)",
        help_text="使用谷电能(度)",
        null=True,
        blank=True
    )
    deep_valley_epi = models.FloatField(
        verbose_name="深谷电能码值(度)",
        help_text="深谷电能码值(度)",
        null=True,
        blank=True
    )
    used_deep_valley_epi = models.FloatField(
        verbose_name="使用深谷电能(度)",
        help_text="使用深谷电能(度)",
        null=True,
        blank=True
    )
    used_amount = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        verbose_name="使用电费(元)",
        help_text='使用电费(元)'
    )
    surplus = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        verbose_name="电费余额(元)",
        help_text='电费余额(元)',
    )
    created_time = models.DateTimeField(
        verbose_name='抄表时间',
        default=timezone.now,
        db_index=True
    )


class EventRecord(models.Model):
    class Meta:
        ordering = ('-id',)
        verbose_name = '预付费系统-事件记录'
        verbose_name_plural = verbose_name

    EVENT_TYPES = (
        ('预警', '预警'),
        ('欠费', '欠费'),
        ('分闸', '分闸'),
        ('合闸', '合闸'),
        ('上线', '上线'),
        ('下线', '下线'),
    )

    el_meter = models.ForeignKey(
        PrepaidElMeter,
        related_name='event_records',
        on_delete=models.PROTECT,
        verbose_name='预付费电表',
        help_text='预付费电表'
    )
    device = models.ForeignKey(
        'equipments.Device',
        on_delete=models.SET_NULL,
        verbose_name='关联设备',
        help_text='关联设备',
        null=True,
        blank=True
    )
    event_type = models.CharField(
        verbose_name="事件类型",
        help_text='事件类型',
        max_length=10,
    )
    created_time = models.DateTimeField(
        verbose_name='时间',
        default=timezone.now
    )


class WithdrawalRecords(models.Model):
    class Meta:
        ordering = ('-id',)
        verbose_name = '预付费系统-提现记录'
        verbose_name_plural = verbose_name

    STATE_ = (
        ('ACCEPTED', '转账已受理'),
        ('WAIT_USER_CONFIRM ', '待收款用户确认'),
        ('TRANSFERING', '转账中'),
        ('SUCCESS', '转账成功'),
        ('FAIL', '转账失败'),
        ('CANCELLED', '转账已撤销')
    )

    org = models.ForeignKey(
        OrgTree,
        on_delete=models.CASCADE,
        verbose_name='所属组织',
        help_text='所属组织'
    )
    user = models.ForeignKey(
        'users.User',  # 使用字符串引用避免循环依赖
        verbose_name="提现用户",
        help_text="提现用户",
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="金额(元)",
        help_text='金额(元)'
    )
    operating_time = models.DateTimeField(
        verbose_name='提现时间',
        help_text='提现时间',
        default=timezone.now
    )
    surplus = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="余额(元)",
        help_text='余额(元)',
    )
    order_id = models.CharField(
        verbose_name="商户单号",
        help_text='商户单号',
        max_length=100,
        unique=True
    )
    transfer_bill_no= models.CharField(
        verbose_name="微信转账单号",
        help_text='微信转账单号',
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    domain = models.ForeignKey(
        Domain,
        help_text='服务域名',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )
    state = models.CharField(
        verbose_name="单据状态",
        help_text='单据状态',
        max_length=20,
        choices=STATE_,
        default='ACCEPTED'
    )
    is_finished = models.BooleanField(
        default=False,
        verbose_name="是否完结",
        help_text="是否完结",
        db_index=True
    )
    update_time = models.DateTimeField(
        verbose_name="最后一次状态变更时",
        help_text="最后一次状态变更时",
        null=True,
        blank=True
    )
    remark = models.CharField(
        max_length=200,
        verbose_name='订单备注',
        help_text='订单备注',
        null=True,
        blank=True
    )


class ElDailyStatistic(models.Model):
    class Meta:
        verbose_name = '预付费系统-电表每日统计'
        verbose_name_plural = verbose_name

    el_meter = models.ForeignKey(
        PrepaidElMeter,
        on_delete=models.PROTECT,
        verbose_name='预付费电表',
        help_text='预付费电表'
    )
    statistic_date = models.DateField(
        verbose_name='统计日期',
        help_text='统计日期'
    )
    used_el = models.FloatField(
        verbose_name="耗电量(度)",
        help_text='耗电量(度)'
    )
    used_amount = models.DecimalField(
        verbose_name="电费(元)",
        help_text='电费(元)',
        max_digits=22,
        decimal_places=10,
        default=0
    )
