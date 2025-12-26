from django.db import models
from backend.apps.custom_perm.models import BaseModel


class AirConditioner(BaseModel):
    """
    中央空调监控
    """
    SWITCH_MAP_ = (
         ('1', '开机'),
         ('0', '关机')
    )
    MODE_MAP_ = (
         ('cool', '制冷'),
         ('heat', '制热'),
         ('auto', '自动'),
         ('dry', '除湿'),
         ('fan', '送风'),
    )
    SPEED_MAP_ = (
         ('auto', '自动'),
         ('high', '高'),
         ('medium', '中'),
         ('low', '低'),
    )
    ATTR_MAP = {
        'host_code': {
            'key': 'host_code',
            'name': '主机编号',
            'data_type': 'T',
        },
        'brand': {
            'key': '空调品牌',
            'name': '空调品牌',
            'data_type': 'T',
        },
        'c_type': {
            'key': 'c_type',
            'name': '品牌类型',
            'data_type': 'T'
        },
        'capacity': {
            'key': 'capacity',
            'name': '容量',
            'data_type': 'N'
        },
        'err_code': {
            'key': 'err_code',
            'name': '故障代码',
            'data_type': 'T'
        },
        'lock_switch': {
            'key': 'lock_switch',
            'name': '是否开关锁定',
            'data_type': 'B'
        },
        'mode_lock': {
            'key': 'mode_lock',
            'name': '是否锁定模式',
            'data_type': 'B'
        },
        'temp_lock': {
            'key': 'temp_lock',
            'name': '是否锁定温度',
            'data_type': 'B'
        },
        't_high_limit': {
            'key': 'temp_room',
            'name': '温度上限',
            'data_type': 'N'
        },
        't_low_limit': {
            'key': 'temp_room',
            'name': '设定温度',
            'data_type': 'N'
        },
        'switch': {
            'key': 'switch',
            'name': '开关状态',
            'data_type': 'B'
        },
        'lock_status': {
            'key': 'lock_status',
            'name': '锁定状态',
            'data_type': 'B'
        },
        'mode': {
            'key': 'mode',
            'name': '模式',
            'data_type': 'T',
        },
        'speed': {
            'key': 'speed',
            'name': '风速',
            'data_type': 'T',
        },
        'temp_room': {
            'key': 'temp_room',
            'name': '室内温度',
            'data_type': 'N'
        },
        'temp_set': {
            'key': 'temp_room',
            'name': '设定温度',
            'data_type': 'N'
        },
        'temp_server': {
            'key': 'temp_room',
            'name': '空调内机温度',
            'data_type': 'N'
        }
    }

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='air_cond',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    host_code = models.CharField(
        verbose_name='主机编号',
        help_text='主机编号',
        max_length=60,
        null=True,
        blank=True
    )
    brand = models.CharField(
        verbose_name='空调品牌',
        help_text='容量',
        max_length=50,
        null=True,
        blank=True
    )
    c_type = models.CharField(
        verbose_name='品牌类型',
        help_text='品牌类型',
        max_length=50,
        null=True,
        blank=True
    )
    capacity = models.CharField(
        verbose_name='容量',
        help_text='容量',
        max_length=50,
        null=True,
        blank=True
    )
    err_code = models.CharField(
        verbose_name='故障代码',
        help_text='故障代码',
        max_length=50,
        null=True,
        blank=True
    )
    lock_status = models.BooleanField(
        default=False,
        verbose_name='锁定状态',
        help_text='锁定状态'
    )
    lock_switch = models.BooleanField(
        default=False,
        verbose_name='是否开关锁定',
        help_text='是否开关锁定'
    )
    temp_lock = models.BooleanField(
        default=False,
        verbose_name='是否锁定温度',
        help_text='是否开关锁定'
    )
    t_high_limit = models.IntegerField(
        verbose_name='温度上限',
        help_text='温度上限',
        null=True,
        blank=True,
    )
    t_low_limit = models.IntegerField(
        verbose_name='温度下限',
        help_text='温度下限',
        null=True,
        blank=True,
    )
    mode_lock = models.BooleanField(
        default=False,
        verbose_name='是否锁定模式',
        help_text='是否锁定模式'
    )
    switch = models.CharField(
        verbose_name='开关状态',
        help_text='开关状态',
        max_length=1,
        null=True,
        blank=True
    )
    mode = models.CharField(
        verbose_name='当前模式',
        help_text='当前模式',
        max_length=20,
        null=True,
        blank=True
    )
    speed = models.CharField(
        verbose_name='风速',
        help_text='风速',
        max_length=20,
        null=True,
        blank=True,
    )
    temp_room = models.FloatField(
         verbose_name='室内温度',
         help_text='室内温度',
         null=True,
         blank=True,
    )
    temp_set = models.FloatField(
         verbose_name='设定温度',
         help_text='设定温度',
         null=True,
         blank=True,
    )
    temp_server = models.FloatField(
         verbose_name='服务器温度',
         help_text='服务器温度',
         null=True,
         blank=True,
    )

    class Meta:
        verbose_name = '设备模型-中央空调监控'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class PersonnelSensor(BaseModel):
    """
    人体存在感应传感器设备模型
    """
    STATUS_MAP_ = (
        ('1', '有人'),
        ('0', '无人'),
    )
    ATTR_MAP = {
        'status': {
            'key': 'status',
            'name': '人员状态',
            'data_type': 'T',
        }
    }
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='personnel_sensor',
        on_delete=models.CASCADE,
        verbose_name='加油站站点',
        help_text='加油站站点'
    )
    status = models.CharField(
        verbose_name='人员状态',
        help_text='人员状态',
        max_length=10,
        db_index=True,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备模型-人体存在传感器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class SpaceTightSensor(BaseModel):
    """
    门窗传感器
    """

    STATUS_MAP_ = (
        ('close', '开'),
        ('open', '关'),
    )
    ATTR_MAP = {
        'status': {
            'key': 'status',
            'name': '门窗状态',
            'data_type': 'T',
        }
    }
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='space_tight_sensor',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    status = models.CharField(
        verbose_name='门窗状态',
        help_text='门窗状态',
        max_length=10,
        db_index=True,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备模型-门窗传感器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class ElectricMeter(BaseModel):
    """
    电表模型
    """

    ATTR_MAP = {
        'epi': {
            'key': 'epi',
            'name': '总有功电能',
            'data_type': 'N',
        },
    }
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='electric_meter',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    epi = models.FloatField(
        verbose_name='有功电能',
        help_text='有功电能',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备模型-电表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class IotBreaker(BaseModel):
    """
    ‌物联网断路器
    """

    ATTR_MAP = {
        'state': {
            'key': 'state',
            'name': '断路器主状态',
            'data_type': 'N'
        },
        'state_sub': {
            'key': 'state_sub',
            'name': '断路器子状态',
            'data_type': 'N'
        },
        'cmd_switch': {
            'key': 'cmd_switch',
            'name': '断路器控制',
            'data_type': 'N'
        },
        'cmd_trip': {
            'key': 'cmd_trip',
            'name': '脱扣',
            'data_type': 'N'
        },
        'cmd_lock': {
            'key': 'cmd_lock',
            'name': '挂锁控制',
            'data_type': 'N'
        },
        'cmd_force_state': {
            'key': 'cmd_force_state',
            'name': '强制合闸',
            'data_type': 'N'
        },
        'cmd_leakage_test': {
            'key': 'cmd_leakage_test',
            'name': '漏电自检',
            'data_type': 'N'
        },
        'cmd_clr_bat': {
            'key': 'cmd_clr_bat',
            'name': '电量清零',
            'data_type': 'N'
        },
        'hz': {
            'key': 'hz',
            'name': '频率',
            'data_type': 'N'
        },
        'ma': {
            'key': 'ma',
            'name': '漏电流',
            'data_type': 'N'
        },
        'rated_u': {
            'key': 'rated_u',
            'name': '额定电压',
            'data_type': 'N'
        },
        'rated_i': {
            'key': 'rated_i',
            'name': '额定电流',
            'data_type': 'N'
        },
        'ua': {
            'key': 'ua',
            'name': 'A相电压',
            'data_type': 'N'
        },
        'ub': {
            'key': 'ub',
            'name': 'B相电压',
            'data_type': 'N'
        },
        'uc': {
            'key': 'uc',
            'name': 'C相电压',
            'data_type': 'N'
        },
        'ia': {
            'key': 'ia',
            'name': 'A相电流',
            'data_type': 'N'
        },
        'ib': {
            'key': 'ib',
            'name': 'B相电流',
            'data_type': 'N'
        },
        'ic': {
            'key': 'ic',
            'name': 'C相电流',
            'data_type': 'N'
        },
        'epi': {
            'key': 'epi',
            'name': '总有功电能',
            'data_type': 'N',
        },
        'p': {
            'key': 'p',
            'name': '总有功功率',
            'data_type': 'N',
        },
        'pa': {
            'key': 'pa',
            'name': 'A相有功功率',
            'data_type': 'N',
        },
        'pb': {
            'key': 'pb',
            'name': 'B相有功功率',
            'data_type': 'N',
        },
        'pc': {
            'key': 'pc',
            'name': 'C相有功功率',
            'data_type': 'N',
        },
        'limit_p': {
            'key': 'limit_p',
            'name': '限额功率',
            'data_type': 'N',
        },
        'qa': {
            'key': 'qa',
            'name': 'A相无功功率',
            'data_type': 'N',
        },
        'qb': {
            'key': 'qb',
            'name': 'B相无功功率',
            'data_type': 'N',
        },
        'qc': {
            'key': 'qc',
            'name': 'C相无功功率',
            'data_type': 'N',
        },
        'pf': {
            'key': 'pf',
            'name': '总功率因数',
            'data_type': 'N',
        },
        'pfa': {
            'key': 'pfa',
            'name': 'A相功率因数',
            'data_type': 'N',
        },
        'pfb': {
            'key': 'pfb',
            'name': 'B相功率因数',
            'data_type': 'N',
        },
        'pfc': {
            'key': 'pfc',
            'name': 'C相功率因数',
            'data_type': 'N',
        },
        'sa': {
            'key': 'sa',
            'name': 'A相视在功率',
            'data_type': 'N',
        },
        'sb': {
            'key': 'sb',
            'name': 'B相视在功率',
            'data_type': 'N',
        },
        'sc': {
            'key': 'sc',
            'name': 'C相视在功率',
            'data_type': 'N',
        },
        't01': {
            'key': 't01',
            'name': '温度1',
            'data_type': 'N',
        },
        't02': {
            'key': 't02',
            'name': '温度2',
            'data_type': 'N',
        },
        't03': {
            'key': 't03',
            'name': '温度3',
            'data_type': 'N',
        },
        't04': {
            'key': 't04',
            'name': '温度4',
            'data_type': 'N',
        },
        't_alarm': {
            'key': 't_alarm',
            'name': '温度报警状态',
            'data_type': 'N',
        },
        't_log': {
            'key': 't_log',
            'name': '温度报警信息',
            'data_type': 'O',
        },
        'gl_alarm': {
            'key': 'gl_alarm',
            'name': '过流报警状态',
            'data_type': 'N',
        },
        'gl_log': {
            'key': 'gl_log',
            'name': '过流报警信息',
            'data_type': 'O',
        },
        'qy_alarm': {
            'key': 'qy_alarm',
            'name': '欠压报警状态',
            'data_type': 'N',
        },
        'qy_log': {
            'key': 'qy_log',
            'name': '欠压报警信息',
            'data_type': 'O',
        },
        'gy_alarm': {
            'key': 'gy_alarm',
            'name': '过压报警状态',
            'data_type': 'N',
        },
        'gy_log': {
            'key': 'gy_log',
            'name': '过压报警信息',
            'data_type': 'O',
        },
        'ld_alarm': {
            'key': 'ld_alarm',
            'name': '漏电报警状态',
            'data_type': 'N',
        },
        'ld_log': {
            'key': 'ld_log',
            'name': '漏电报警信息',
            'data_type': 'O',
        },
        'dl_alarm': {
            'key': 'dl_alarm',
            'name': '短路报警状态',
            'data_type': 'N',
        },
        'dl_log': {
            'key': 'dl_log',
            'name': '短路报警信息',
            'data_type': 'O',
        }
    }

    STATE_MAP_ = (
        (1, '闭合'),
        (2, '断开'),
    )
    STATE_SUB_MAP_ = (
        (1, '远程闭合'),
        (2, '远程断开'),
        (5, '手动闭合'),
        (6, '手动断开'),
        (9, '闭合/挂锁'),
        (10, '断开/挂锁'),
    )
    ERR_STATE_MAP_ = (
        ('normal', '正常'),
        ('warming', '预警'),
        ('alerting', '告警')
    )

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='iot_breakers',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    state = models.IntegerField(
         verbose_name='断路器主状态',
         help_text='断路器主状态',
         null=True,
         blank=True,
    )
    state_sub = models.IntegerField(
        verbose_name='断路器子状态',
        help_text='断路器子状态',
        null=True,
        blank=True,
    )
    cmd_switch = models.IntegerField(
        verbose_name='断路器控制',
        help_text='断路器控制',
        null=True,
        blank=True,
    )
    cmd_trip = models.IntegerField(
         verbose_name='脱扣',
         help_text='脱扣',
         null=True,
         blank=True,
    )
    cmd_lock = models.IntegerField(
         verbose_name='挂锁控制',
         help_text='挂锁控制',
         null=True,
         blank=True,
    )
    cmd_force_state = models.IntegerField(
         verbose_name='强制合闸',
         help_text='强制合闸',
         null=True,
         blank=True,
    )
    cmd_leakage_test = models.IntegerField(
         verbose_name='漏电自检',
         help_text='漏电自检',
         null=True,
         blank=True,
    )
    cmd_clr_bat = models.IntegerField(
        verbose_name='电量清零',
        help_text='电量清零',
        null=True,
        blank=True,
    )
    hz = models.FloatField(
         verbose_name='频率',
         help_text='频率',
         null=True,
         blank=True,
    )
    ma = models.FloatField(
         verbose_name='漏电流',
         help_text='漏电流',
         null=True,
         blank=True,
    )
    rated_u = models.FloatField(
         verbose_name='额定电压',
         help_text='额定电压',
         null=True,
         blank=True,
    )
    rated_i = models.FloatField(
         verbose_name='额定电流',
         help_text='额定电流',
         null=True,
         blank=True,
    )
    ua = models.FloatField(
         verbose_name='A相电压',
         help_text='A相电压',
         null=True,
         blank=True,
    )
    ub = models.FloatField(
         verbose_name='B相电压',
         help_text='B相电压',
         null=True,
         blank=True,
    )
    uc = models.FloatField(
         verbose_name='C相电压',
         help_text='C相电压',
         null=True,
         blank=True,
    )
    ia = models.FloatField(
        verbose_name='A相电流',
        help_text='A相电流',
        null=True,
        blank=True,
    )
    ib = models.FloatField(
         verbose_name='B相电流',
         help_text='B相电流',
         null=True,
         blank=True,
    )
    ic = models.FloatField(
         verbose_name='C相电流',
         help_text='C相电流',
         null=True,
         blank=True,
    )
    epi = models.FloatField(
         verbose_name='总有功电能',
         help_text='总有功电能',
         null=True,
         blank=True,
    )
    p = models.FloatField(
        verbose_name='总有功功率',
        help_text='总有功功率',
        null=True,
        blank=True,
    )
    pa = models.FloatField(
         verbose_name='A相有功功率',
         help_text='A相有功功率',
         null=True,
         blank=True,
    )
    pb = models.FloatField(
         verbose_name='B相有功功率',
         help_text='B相有功功率',
         null=True,
         blank=True,
    )
    pc = models.FloatField(
         verbose_name='C相有功功率',
         help_text='C相有功功率',
         null=True,
         blank=True,
    )
    limit_p = models.FloatField(
        verbose_name='限额功率',
        help_text='限额功率',
        null=True,
        blank=True,
    )
    qa = models.FloatField(
         verbose_name='A相无功功率',
         help_text='A相无功功率',
         null=True,
         blank=True,
    )
    qb = models.FloatField(
         verbose_name='B相无功功率',
         help_text='B相无功功率',
         null=True,
         blank=True,
    )
    qc = models.FloatField(
         verbose_name='C相无功功率',
         help_text='C相无功功率',
         null=True,
         blank=True,
    )
    pf = models.FloatField(
        verbose_name='总功率因数',
        help_text='总功率因数',
        null=True,
        blank=True,
    )
    pfa = models.FloatField(
         verbose_name='A相功率因数',
         help_text='A相功率因数',
         null=True,
         blank=True,
    )
    pfb = models.FloatField(
         verbose_name='B相功率因数',
         help_text='B相功率因数',
         null=True,
         blank=True,
    )
    pfc = models.FloatField(
         verbose_name='C相功率因数',
         help_text='C相功率因数',
         null=True,
         blank=True,
    )
    sa = models.FloatField(
         verbose_name='A相视在功率',
         help_text='A相视在功率',
         null=True,
         blank=True,
    )
    sb = models.FloatField(
         verbose_name='B相视在功率',
         help_text='B相视在功率',
         null=True,
         blank=True,
    )
    sc = models.FloatField(
         verbose_name='C相视在功率',
         help_text='C相视在功率',
         null=True,
         blank=True,
         )
    t01 = models.FloatField(
         verbose_name='温度1',
         help_text='温度1',
         null=True,
         blank=True,
    )
    t02 = models.FloatField(
         verbose_name='温度2',
         help_text='温度2',
         null=True,
         blank=True,
    )
    t03 = models.FloatField(
         verbose_name='温度3',
         help_text='温度3',
         null=True,
         blank=True,
    )
    t04 = models.FloatField(
         verbose_name='温度4',
         help_text='温度4',
         null=True,
         blank=True,
    )
    t_alarm = models.IntegerField(
         verbose_name='温度报警状态',
         help_text='温度报警状态',
         null=True,
         blank=True,
    )
    t_log = models.JSONField(
         verbose_name='温度报警信息',
         help_text='温度报警信息',
         null=True,
         blank=True,
    )
    gl_alarm = models.IntegerField(
         verbose_name='过流报警状态',
         help_text='过流报警状态',
         null=True,
         blank=True,
    )
    gl_log = models.JSONField(
         verbose_name='过流报警信息',
         help_text='过流报警信息',
         null=True,
         blank=True,
    )
    qy_alarm = models.IntegerField(
         verbose_name='欠压报警状态',
         help_text='欠压报警状态',
         null=True,
         blank=True,
    )
    qy_log = models.JSONField(
         verbose_name='欠压报警信息',
         help_text='欠压报警信息',
         null=True,
         blank=True,
    )
    gy_alarm = models.IntegerField(
         verbose_name='过压报警状态',
         help_text='过压报警状态',
         null=True,
         blank=True,
    )
    gy_log = models.JSONField(
         verbose_name='过压报警信息',
         help_text='过压报警信息',
         null=True,
         blank=True,
    )
    ld_alarm = models.IntegerField(
         verbose_name='漏电报警状态',
         help_text='漏电报警状态',
         null=True,
         blank=True,
    )
    ld_log = models.JSONField(
         verbose_name='漏电报警信息',
         help_text='漏电报警信息',
         null=True,
         blank=True,
    )
    dl_alarm = models.IntegerField(
         verbose_name='短路报警状态',
         help_text='短路报警状态',
         null=True,
         blank=True,
    )
    dl_log = models.JSONField(
         verbose_name='短路报警信息',
         help_text='短路报警信息',
         null=True,
         blank=True,
    )

    class Meta:
        verbose_name = '设备模型-物联网断路器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class PowerSource(BaseModel):
    """
    设备模型-进线电源
    """

    ATTR_MAP = {
        'epi': {
            'key': 'epi',
            'name': '总有功电能',
            'data_type': 'N',
        },
        'p': {
            'key': 'p',
            'name': '总有功功率',
            'data_type': 'N',
        }

    }
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='power_source',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    epi = models.FloatField(
        verbose_name='有功电能',
        help_text='有功电能',
        null=True,
        blank=True
    )
    p = models.FloatField(
        verbose_name='总有功功率',
        help_text='总有功功率',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '设备模型-进线电源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class HiddenDangerMonitor(BaseModel):
    """
    设备模型-隐患监测
    """

    ATTR_MAP = {
        't01': {
            'key': 't01',
            'name': '温度1',
            'data_type': 'N',
        },
        't02': {
            'key': 't02',
            'name': '温度2',
            'data_type': 'N',
        },
        't03': {
            'key': 't03',
            'name': '温度3',
            'data_type': 'N',
        },
        't04': {
            'key': 't04',
            'name': '温度4',
            'data_type': 'N',
        },
        'ma': {
            'key': 'ma',
            'name': '漏电流',
            'data_type': 'N'
        },
        'p': {
            'key': 'p',
            'name': '总有功功率',
            'data_type': 'N',
        }

    }
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='hidden_danger_monitor',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    t01 = models.FloatField(
        verbose_name='温度1',
        help_text='温度1',
        null=True,
        blank=True,
    )
    t02 = models.FloatField(
        verbose_name='温度2',
        help_text='温度2',
        null=True,
        blank=True,
    )
    t03 = models.FloatField(
        verbose_name='温度3',
        help_text='温度3',
        null=True,
        blank=True,
    )
    t04 = models.FloatField(
        verbose_name='温度4',
        help_text='温度4',
        null=True,
        blank=True,
    )
    ma = models.FloatField(
        verbose_name='漏电流',
        help_text='漏电流',
        null=True,
        blank=True,
    )
    p = models.FloatField(
        verbose_name='总有功功率',
        help_text='总有功功率',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '设备模型-隐患监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class ElMonitorInstrument(BaseModel):
    """
    三项电力仪表
    """
    ATTR_MAP = {
        'u0': {
            'key': 'u0',
            'name': '零序电压',
            'data_type': 'N'
        },
        'i0': {
            'key': 'i0',
            'name': '零序电流',
            'data_type': 'N'
        },
        'ua': {
            'key': 'ua',
            'name': 'A相电压',
            'data_type': 'N'
        },
        'ub': {
            'key': 'ub',
            'name': 'B相电压',
            'data_type': 'N'
        },
        'uc': {
            'key': 'uc',
            'name': 'C相电压',
            'data_type': 'N'
        },
        'ia': {
            'key': 'ia',
            'name': 'A相电流',
            'data_type': 'N'
        },
        'ib': {
            'key': 'ib',
            'name': 'B相电流',
            'data_type': 'N'
        },
        'ic': {
            'key': 'ic',
            'name': 'C相电流',
            'data_type': 'N'
        },
        'hz': {
            'key': 'hz',
            'name': '频率',
            'data_type': 'N'
        },
        'p': {
            'key': 'p',
            'name': '总有功功率',
            'data_type': 'N',
        },
        'pa': {
            'key': 'pa',
            'name': 'A相有功功率',
            'data_type': 'N',
        },
        'pb': {
            'key': 'pb',
            'name': 'B相有功功率',
            'data_type': 'N',
        },
        'pc': {
            'key': 'pc',
            'name': 'C相有功功率',
            'data_type': 'N',
        },
        'qa': {
            'key': 'qa',
            'name': 'A相无功功率',
            'data_type': 'N',
        },
        'qb': {
            'key': 'qb',
            'name': 'B相无功功率',
            'data_type': 'N',
        },
        'qc': {
            'key': 'qc',
            'name': 'C相无功功率',
            'data_type': 'N',
        },
        'q': {
            'key': 'q',
            'name': '无功功率',
            'data_type': 'N',
        },
        'pf': {
            'key': 'pf',
            'name': '总功率因数',
            'data_type': 'N',
        },
        'pfa': {
            'key': 'pfa',
            'name': 'A相功率因数',
            'data_type': 'N',
        },
        'pfb': {
            'key': 'pfb',
            'name': 'B相功率因数',
            'data_type': 'N',
        },
        'pfc': {
            'key': 'pfc',
            'name': 'C相功率因数',
            'data_type': 'N',
        },
        'sa': {
            'key': 'sa',
            'name': 'A相视在功率',
            'data_type': 'N',
        },
        'sb': {
            'key': 'sb',
            'name': 'B相视在功率',
            'data_type': 'N',
        },
        'sc': {
            'key': 'sc',
            'name': 'C相视在功率',
            'data_type': 'N',
        },
        's': {
            'key': 's',
            'name': '总视在功率',
            'data_type': 'N',
        },
        'epi': {
            'key': 'epi',
            'name': '正向有功总电能',
            'data_type': 'N',
        },
        'epe': {
            'key': 'epe',
            'name': '反向有功总电能',
            'data_type': 'N',
        },
        'eql': {
            'key': 'eql',
            'name': '正向无功总电能',
            'data_type': 'N',
        },
        'eqc': {
            'key': 'eqc',
            'name': '反向无功总电能',
            'data_type': 'N',
        }
    }

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='el_monitor_instrument',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    u0 = models.FloatField(
         verbose_name='零序电压',
         help_text='零序电压',
         null=True,
         blank=True,
    )
    ua = models.FloatField(
         verbose_name='A相电压',
         help_text='A相电压',
         null=True,
         blank=True,
    )
    ub = models.FloatField(
         verbose_name='B相电压',
         help_text='B相电压',
         null=True,
         blank=True,
    )
    uc = models.FloatField(
         verbose_name='C相电压',
         help_text='C相电压',
         null=True,
         blank=True,
    )
    ia = models.FloatField(
        verbose_name='A相电流',
        help_text='A相电流',
        null=True,
        blank=True,
    )
    ib = models.FloatField(
         verbose_name='B相电流',
         help_text='B相电流',
         null=True,
         blank=True,
    )
    ic = models.FloatField(
         verbose_name='C相电流',
         help_text='C相电流',
         null=True,
         blank=True,
    )
    i0 = models.FloatField(
        verbose_name='零序电流',
        help_text='零序电流',
        null=True,
        blank=True,
    )
    hz = models.FloatField(
        verbose_name='频率',
        help_text='频率',
        null=True,
        blank=True,
    )
    epi = models.FloatField(
         verbose_name='正向有功总电能',
         help_text='正向有功总电能',
         null=True,
         blank=True,
    )
    epe = models.FloatField(
        verbose_name='反向有功总电能',
        help_text='反向有功总电能',
        null=True,
        blank=True,
    )
    eql = models.FloatField(
        verbose_name='正向无功总电能',
        help_text='正向无功总电能',
        null=True,
        blank=True,
    )
    eqc = models.FloatField(
        verbose_name='反向无功总电能',
        help_text='反向无功总电能',
        null=True,
        blank=True,
    )
    p = models.FloatField(
        verbose_name='总有功功率',
        help_text='总有功功率',
        null=True,
        blank=True,
    )
    pa = models.FloatField(
         verbose_name='A相有功功率',
         help_text='A相有功功率',
         null=True,
         blank=True,
    )
    pb = models.FloatField(
         verbose_name='B相有功功率',
         help_text='B相有功功率',
         null=True,
         blank=True,
    )
    pc = models.FloatField(
         verbose_name='C相有功功率',
         help_text='C相有功功率',
         null=True,
         blank=True,
    )
    qa = models.FloatField(
         verbose_name='A相无功功率',
         help_text='A相无功功率',
         null=True,
         blank=True,
    )
    qb = models.FloatField(
         verbose_name='B相无功功率',
         help_text='B相无功功率',
         null=True,
         blank=True,
    )
    qc = models.FloatField(
         verbose_name='C相无功功率',
         help_text='C相无功功率',
         null=True,
         blank=True,
    )
    q = models.FloatField(
        verbose_name='无功功率',
        help_text='无功功率',
        null=True,
        blank=True,
    )
    pfa = models.FloatField(
         verbose_name='A相功率因数',
         help_text='A相功率因数',
         null=True,
         blank=True,
    )
    pfb = models.FloatField(
         verbose_name='B相功率因数',
         help_text='B相功率因数',
         null=True,
         blank=True,
    )
    pfc = models.FloatField(
         verbose_name='C相功率因数',
         help_text='C相功率因数',
         null=True,
         blank=True,
    )
    pf = models.FloatField(
        verbose_name='总功率因数',
        help_text='总功率因数',
        null=True,
        blank=True,
    )
    sa = models.FloatField(
         verbose_name='A相视在功率',
         help_text='A相视在功率',
         null=True,
         blank=True,
    )
    sb = models.FloatField(
         verbose_name='B相视在功率',
         help_text='B相视在功率',
         null=True,
         blank=True,
    )
    sc = models.FloatField(
         verbose_name='C相视在功率',
         help_text='C相视在功率',
         null=True,
         blank=True,
    )
    s = models.FloatField(
        verbose_name='总视在功率',
        help_text='总视在功率',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '设备模型-三项电力仪表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class Transformer(BaseModel):
    """
    变压器电力监测
    """

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='transformer',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    ua = models.FloatField(
         verbose_name='A相电压',
         help_text='A相电压',
         null=True,
         blank=True,
    )
    ub = models.FloatField(
         verbose_name='B相电压',
         help_text='B相电压',
         null=True,
         blank=True,
    )
    uc = models.FloatField(
         verbose_name='C相电压',
         help_text='C相电压',
         null=True,
         blank=True,
    )
    uab = models.FloatField(
         verbose_name='AB线电压',
         help_text='AB线电压',
         null=True,
         blank=True,
    )
    ubc = models.FloatField(
         verbose_name='BC线电压',
         help_text='BC线电压',
         null=True,
         blank=True,
    )
    uca = models.FloatField(
         verbose_name='CA线电压',
         help_text='CA线电压',
         null=True,
         blank=True,
    )
    hz = models.FloatField(
        verbose_name='频率',
        help_text='频率',
        null=True,
        blank=True,
    )
    ia = models.FloatField(
        verbose_name='A相电流',
        help_text='A相电流',
        null=True,
        blank=True,
    )
    ib = models.FloatField(
         verbose_name='B相电流',
         help_text='B相电流',
         null=True,
         blank=True,
    )
    ic = models.FloatField(
         verbose_name='C相电流',
         help_text='C相电流',
         null=True,
         blank=True,
    )
    i0 = models.FloatField(
        verbose_name='零序电流',
        help_text='零序电流',
        null=True,
        blank=True,
    )
    s = models.FloatField(
        verbose_name='总视在功率',
        help_text='总视在功率',
        null=True,
        blank=True,
    )
    sa = models.FloatField(
        verbose_name='A相视在功率',
        help_text='A相视在功率',
        null=True,
        blank=True,
    )
    sb = models.FloatField(
        verbose_name='B相视在功率',
        help_text='B相视在功率',
        null=True,
        blank=True,
    )
    sc = models.FloatField(
        verbose_name='C相视在功率',
        help_text='C相视在功率',
        null=True,
        blank=True,
    )
    p = models.FloatField(
        verbose_name='总有功功率',
        help_text='总有功功率',
        null=True,
        blank=True,
    )
    pa = models.FloatField(
        verbose_name='A相有功功率',
        help_text='A相有功功率',
        null=True,
        blank=True,
    )
    pb = models.FloatField(
        verbose_name='B相有功功率',
        help_text='B相有功功率',
        null=True,
        blank=True,
    )
    pc = models.FloatField(
        verbose_name='C相有功功率',
        help_text='C相有功功率',
        null=True,
        blank=True,
    )
    q = models.FloatField(
        verbose_name='无功功率',
        help_text='无功功率',
        null=True,
        blank=True,
    )
    qa = models.FloatField(
        verbose_name='A相无功功率',
        help_text='A相无功功率',
        null=True,
        blank=True,
    )
    qb = models.FloatField(
        verbose_name='B相无功功率',
        help_text='B相无功功率',
        null=True,
        blank=True,
    )
    qc = models.FloatField(
        verbose_name='C相无功功率',
        help_text='C相无功功率',
        null=True,
        blank=True,
    )
    pf = models.FloatField(
        verbose_name='总功率因数',
        help_text='总功率因数',
        null=True,
        blank=True,
    )
    pfa = models.FloatField(
        verbose_name='A相功率因数',
        help_text='A相功率因数',
        null=True,
        blank=True,
    )
    pfb = models.FloatField(
        verbose_name='B相功率因数',
        help_text='B相功率因数',
        null=True,
        blank=True,
    )
    pfc = models.FloatField(
        verbose_name='C相功率因数',
        help_text='C相功率因数',
        null=True,
        blank=True,
    )
    uunb = models.FloatField(
        verbose_name='电压不平衡度',
        help_text='电压不平衡度',
        null=True,
        blank=True,
    )
    iunb = models.FloatField(
        verbose_name='电流不平衡度',
        help_text='电流不平衡度',
        null=True,
        blank=True,
    )
    epi_demand = models.FloatField(
        verbose_name='当前正向有功需量',
        help_text='当前正向有功需量',
        null=True,
        blank=True,
    )
    epe_demand = models.FloatField(
        verbose_name='当前反向有功需量',
        help_text='当前反向有功需量',
        null=True,
        blank=True,
    )
    eql_demand = models.FloatField(
        verbose_name='当前正向无功需量',
        help_text='当前正向无功需量',
        null=True,
        blank=True,
    )
    eqc_demand = models.FloatField(
        verbose_name='当前反向无功需量',
        help_text='当前反向无功需量',
        null=True,
        blank=True,
    )
    epi = models.FloatField(
         verbose_name='正向有功总电能',
         help_text='正向有功总电能',
         null=True,
         blank=True,
    )
    thdu_ua = models.FloatField(
        verbose_name='A相谐波电压总畸变率',
        help_text='A相谐波电压总畸变率',
        null=True,
        blank=True,
    )
    thdu_ub = models.FloatField(
        verbose_name='B相谐波电压总畸变率',
        help_text='B相谐波电压总畸变率',
        null=True,
        blank=True,
    )
    thdu_uc = models.FloatField(
        verbose_name='C相谐波电压总畸变率',
        help_text='C相谐波电压总畸变率',
        null=True,
        blank=True,
    )
    thdi_ia = models.FloatField(
        verbose_name='A相谐波电流总畸变率',
        help_text='A相谐波电流总畸变率',
        null=True,
        blank=True,
    )
    thdi_ib = models.FloatField(
        verbose_name='B相谐波电流总畸变率',
        help_text='B相谐波电流总畸变率',
        null=True,
        blank=True,
    )
    thdi_ic = models.FloatField(
        verbose_name='C相谐波电流总畸变率',
        help_text='C相谐波电流总畸变率',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '设备模型-变压器电力监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class TfTemperatureMonitor(BaseModel):
    """
    设备模型-变压器温度监测
    """

    ATTR_MAP = {
        't01': {
            'key': 't01',
            'name': 'A项绕组温度',
            'data_type': 'N',
        },
        't02': {
            'key': 't02',
            'name': 'B项绕组温度',
            'data_type': 'N',
        },
        't03': {
            'key': 't03',
            'name': 'C项绕组温度',
            'data_type': 'N',
        },
    }
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='tf_temperature_monitor',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    t01 = models.FloatField(
        verbose_name='温度1',
        help_text='温度1',
        null=True,
        blank=True,
    )
    t02 = models.FloatField(
        verbose_name='温度2',
        help_text='温度2',
        null=True,
        blank=True,
    )
    t03 = models.FloatField(
        verbose_name='温度3',
        help_text='温度3',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '设备模型-变压器温度监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class LightMonitor(BaseModel):
    """
    设备模型-照明设备
    """
    ATTR_MAP = {
        f'{key}{i}': {
            'key': f'{key}{i}',
            'name': f'回路{i}{key_text}',
            'data_type': data_type,
        } for i in range(1, 17) for key, key_text, data_type in [
            ('state', '状态', 'N'),
            ('brightness', '亮度', 'N'),
            ('switch', '开关控制', 'N'),
            ('adjust', '亮度调节', 'N')
        ]
    }
    DOWN_ATTR_MAP = {
        'switch': {
            'key': 'switch',
            'name': '照明一键开关',
            'data_type': 'N',
        },
        'adjust': {
            'key': 'adjust',
            'name': '亮度一键调节',
            'data_type': 'N',
        }
    }
    DOWN_ATTR_MAP.update(ATTR_MAP)

    # 排除属性
    EXCLUDE_ATTR = ['state', ]

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='light_monitor',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    light_count = models.SmallIntegerField(
        verbose_name='当前亮灯数',
        help_text='当前亮灯数',
        null=True,
        blank=True,
    )
    total_count = models.SmallIntegerField(
        verbose_name='总回路数',
        help_text='总回路数',
        null=True,
        blank=True,
    )
    state = models.SmallIntegerField(
        verbose_name='照明状态',
        help_text='照明状态',
        null=True,
        blank=True,
    )
    light_data = models.JSONField(
        verbose_name='灯具上报数据: {"state1": 1, "brightness1": 100, ...}',
        help_text='灯具上报数据: {"state1": 1, "brightness1": 100, ...}',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备模型-照明设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class SwitchMonitor(BaseModel):
    """
    开关设备
    """
    # 下发属性
    DOWN_ATTR_MAP = {
        'switch': {
            'key': 'switch',
            'name': '一键开关',
            'data_type': 'N',
        },
        'switch1': {
            'key': 'switch1',
            'name': '回路1开关控制',
            'data_type': 'N',
        },
        'switch2': {
            'key': 'switch2',
            'name': '回路2开关控制',
            'data_type': 'N',
        },
        'switch3': {
            'key': 'switch3',
            'name': '回路3开关控制',
            'data_type': 'N',
        },
        'switch4': {
            'key': 'switch4',
            'name': '回路4开关控制',
            'data_type': 'N',
        },
        'switch5': {
            'key': 'switch5',
            'name': '回路5开关控制',
            'data_type': 'N',
        },
        'switch6': {
            'key': 'switch6',
            'name': '回路6开关控制',
            'data_type': 'N',
        },
        'switch7': {
            'key': 'switch7',
            'name': '回路7开关控制',
            'data_type': 'N',
        },
        'switch8': {
            'key': 'switch8',
            'name': '回路8开关控制',
            'data_type': 'N',
        },
        'switch9': {
            'key': 'switch9',
            'name': '回路9开关控制',
            'data_type': 'N',
        },
        'switch10': {
            'key': 'switch10',
            'name': '回路10开关控制',
            'data_type': 'N',
        },
        'switch11': {
            'key': 'switch11',
            'name': '回路11开关控制',
            'data_type': 'N',
        },
        'switch12': {
            'key': 'switch12',
            'name': '回路12开关控制',
            'data_type': 'N',
        },
        'switch13': {
            'key': 'switch13',
            'name': '回路13开关控制',
            'data_type': 'N',
        },
        'switch14': {
            'key': 'switch14',
            'name': '回路14开关控制',
            'data_type': 'N',
        },
        'switch15': {
            'key': 'switch15',
            'name': '回路15开关控制',
            'data_type': 'N',
        },
        'switch16': {
            'key': 'switch16',
            'name': '回路16开关控制',
            'data_type': 'N',
        },
    }
    # 排除属性
    EXCLUDE_ATTR = ['state', ]

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='switch_monitor',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    on_count = models.SmallIntegerField(
        verbose_name='当前闭合回路数',
        help_text='当前闭合回路数',
        null=True,
        blank=True,
    )
    total_count = models.SmallIntegerField(
        verbose_name='总回路数',
        help_text='总回路数',
        null=True,
        blank=True,
    )
    state = models.SmallIntegerField(
        verbose_name='回路状态',
        help_text='回路状态',
        null=True,
        blank=True,
    )
    state1 = models.SmallIntegerField(
        verbose_name='回路1状态',
        help_text='回路1状态',
        null=True,
        blank=True,
    )
    state2 = models.SmallIntegerField(
        verbose_name='回路2状态',
        help_text='回路2状态',
        null=True,
        blank=True,
    )
    state3 = models.SmallIntegerField(
        verbose_name='回路3状态',
        help_text='回路3状态',
        null=True,
        blank=True,
    )
    state4 = models.SmallIntegerField(
        verbose_name='回路4状态',
        help_text='回路4状态',
        null=True,
        blank=True,
    )
    state5 = models.SmallIntegerField(
        verbose_name='回路5状态',
        help_text='回路5状态',
        null=True,
        blank=True,
    )
    state6 = models.SmallIntegerField(
        verbose_name='回路6状态',
        help_text='回路6状态',
        null=True,
        blank=True,
    )
    state7 = models.SmallIntegerField(
        verbose_name='回路7状态',
        help_text='回路7状态',
        null=True,
        blank=True,
    )
    state8 = models.SmallIntegerField(
        verbose_name='回路8状态',
        help_text='回路8状态',
        null=True,
        blank=True,
    )
    state9 = models.SmallIntegerField(
        verbose_name='回路9状态',
        help_text='回路9状态',
        null=True,
        blank=True,
    )
    state10 = models.SmallIntegerField(
        verbose_name='回路10状态',
        help_text='回路10状态',
        null=True,
        blank=True,
    )
    state11 = models.SmallIntegerField(
        verbose_name='回路11状态',
        help_text='回路11状态',
        null=True,
        blank=True,
    )
    state12 = models.SmallIntegerField(
        verbose_name='回路12状态',
        help_text='回路12状态',
        null=True,
        blank=True,
    )
    state13 = models.SmallIntegerField(
        verbose_name='回路13状态',
        help_text='回路13状态',
        null=True,
        blank=True,
    )
    state14 = models.SmallIntegerField(
        verbose_name='回路14状态',
        help_text='回路14状态',
        null=True,
        blank=True,
    )
    state15 = models.SmallIntegerField(
        verbose_name='回路15状态',
        help_text='回路15状态',
        null=True,
        blank=True,
    )
    state16 = models.SmallIntegerField(
        verbose_name='回路16状态',
        help_text='回路16状态',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = '设备模型-开关监控设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class EnvironmentMonitor(BaseModel):
    """
    环境系统设备
    """
    device = models.OneToOneField(
        to='equipments.Device',
        related_name='environment_monitor',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    up_attr_data = models.JSONField(
        verbose_name='属性最近一次上报值',
        help_text='属性最近一次上报值',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '设备模型-环境系统设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name


class PrepaidElectricMeter(BaseModel):
    class Meta:
        verbose_name = '设备模型-预付费电表'
        verbose_name_plural = verbose_name

    device = models.OneToOneField(
        to='equipments.Device',
        related_name='prepaid_electric_meter',
        on_delete=models.CASCADE,
        verbose_name='关联设备',
        help_text='关联设备'
    )
    epi = models.FloatField(
        verbose_name='电表总码值(度)',
        help_text='电表总码值(度)',
        null=True,
        blank=True
    )
    top_epi = models.FloatField(
        verbose_name="尖电能码值(度)",
        help_text="尖电能码值(度)",
        null=True,
        blank=True
    )
    on_peak_epi = models.FloatField(
        verbose_name="峰电能码值(度)",
        help_text="峰电能码值(度)",
        null=True,
        blank=True
    )
    flat_epi = models.FloatField(
        verbose_name="平电能码值(度)",
        help_text="平电能码值(度)",
        null=True,
        blank=True
    )
    valley_epi = models.FloatField(
        verbose_name="谷电能码值(度)",
        help_text="谷电能码值(度)",
        null=True,
        blank=True
    )
    deep_valley_epi = models.FloatField(
        verbose_name="深谷电能码值(度)",
        help_text="深谷电能码值(度)",
        null=True,
        blank=True
    )
    state = models.SmallIntegerField(
        verbose_name='开合状态',
        help_text='开合状态',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.device.name
