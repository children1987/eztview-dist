import datetime
import time
import traceback
import _setup_django

from backend.apps.el_prepayment_servers.biz.tools import org_amount_refund
from backend.apps.el_prepayment_servers.models import RechargeOrder, WithdrawalRecords
from backend.apps.wechat.biz.wx_pay import WechatPayTools
from backend.wechat_pay_server.config import wechat_pay_server_logger as logger
from backend.m_common.debugger import rerun


class WechatPayStateCheck:
    """
    设备状态同步任务 --
        每一小时同步一次（订单状态）
    """

    @staticmethod
    def check_jsapi_recharge_order(end_time):
        """
        JSAPI 充值订单
        """
        recharge_orders = RechargeOrder.objects.filter(
            trade_state__in=['PENDING', 'NOTPAY'],
            trade_type='JSAPI',
            create_time__lte=end_time
        ).select_related('domain')
        for obj in recharge_orders:
            older_state = obj.trade_state
            pay_manager = WechatPayTools(
                appid=obj.domain.we_svc_app_id,
                mchid=obj.domain.we_mch_id,
                serial_no=obj.domain.we_mch_serial_no,
            )
            res = pay_manager.close_order(
                out_trade_no=obj.out_trade_no
            )
            if not str(res.status_code).startswith('2'):
                logger.error(f'订单关闭失败：{obj.out_trade_no}')
                logger.error(f'code：{res.status_code}， err_data: {res.json()}')
                continue
            logger.info(f'{obj.out_trade_no} JSAPI充值订单关闭成功')
            RechargeOrder.objects.filter(
                id=obj.id,
                trade_state=older_state
            ).update(
                trade_state='CLOSED'
            )

    @staticmethod
    def check_withdrawal_order(end_time):
        """
        转账订单
        """
        withdrawal_orders = WithdrawalRecords.objects.filter(
            operating_time__lte=end_time,
            is_finished=False
        ).select_related('domain')
        for obj in withdrawal_orders:
            older_state = obj.state
            pay_manager = WechatPayTools(
                appid=obj.domain.we_svc_app_id,
                mchid=obj.domain.we_mch_id,
                serial_no=obj.domain.we_mch_serial_no,
            )
            res = pay_manager.cancel_transfer(
                out_bill_no=obj.order_id
            )
            if not str(res.status_code).startswith('2'):
                logger.error(f'撤销转账失败：{obj.order_id}')
                logger.error(f'code：{res.status_code}， err_data: {res.json()}')
                continue
            logger.info(f'{obj.order_id} 提现转账订单撤销成功')
            ret = WithdrawalRecords.objects.filter(
                id=obj.id,
                state=older_state,
                is_finished=False
            ).update(
                state='CANCELLED',
                is_finished=True
            )
            if ret:
                org_amount_refund(obj.org_id, obj.amount)

    @classmethod
    def run(cls):
        while 1:
            try:
                c_time = datetime.datetime.now()
                check_time = c_time - datetime.timedelta(minutes=30)
                cls.check_withdrawal_order(check_time)
                cls.check_jsapi_recharge_order(check_time)
            except Exception as _:
                logger.error(traceback.format_exc())
            time.sleep(1800)


@rerun(
    'WechatPayStateCheck 支付订单状态检测重启中',
    logger=logger,
    max_retry_count=3
)
def wxpay_state_check_task():
    checker = WechatPayStateCheck()
    checker.run()


if __name__ == '__main__':
    try:
        wxpay_state_check_task()
    except Exception as err:
        logger.error('WechatPayStateCheck 服务启动失败！')
        logger.error(err)
        logger.error(traceback.format_exc())
