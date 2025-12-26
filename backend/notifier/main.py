import json
import traceback
from copy import deepcopy
import _setup_django
import backend.m_common.set_timezone

from django.contrib.auth import get_user_model
from backend.apps.wechat.biz.mp import WechatPublicAccount
from backend.m_common.dingtalk.dingtalk import SendMsg as SendDingtalk
from backend.m_common.my_email import MyEmail
from backend.m_common.sms.tencent.sms_sender import SMS_ID_MAP, send as send_sms
from backend.m_common.mq_factory import NotifierMq
from backend.notifier.log import logger
from backend.notifier.notify_template import NOTIFY_TEMPLATE

User = get_user_model()


class Notifier(object):
    """
    读取notify MQ 中待发的通知，并通过短信，电子邮件，钉钉群机器人，企业微信群机器人(待实现)，
    飞书机器人（待实现）通知用户
    """

    @staticmethod
    def _sms(aims: list, template_key, params: list, **kwargs):
        """
        以短信的形式通知用户
        """
        sms_id = SMS_ID_MAP[template_key]
        logger.info(f'aims = {aims}, sms_id = {type(sms_id)}{sms_id} , params = {params}')
        send_sms(aims, sms_id, params, logger=logger)

    @staticmethod
    def _email(aims: list, template_key, params: list, **kwargs):
        """
        以email的形式通知用户
        """
        title_params = kwargs['title_params']
        em = MyEmail()
        em_subject_template = NOTIFY_TEMPLATE[template_key]['template']['email']['title']
        em_content_template = NOTIFY_TEMPLATE[template_key]['template']['email']['content']
        em_content_html = em_content_template.format(*params)

        logger.debug(f'content_text={em_content_html}')

        em.Subject = em_subject_template.format(*title_params)
        em.to_list = aims
        em_msg = em.get_mail_content(html_msg=em_content_html)
        em.send(em_msg)

    @classmethod
    def _ding_robot(cls, aims: dict, template_key, params: list, **kwargs):
        """
        以钉钉群消息的形式通知用户
        """
        url = aims['url']
        secret = aims['secret']
        sender = SendDingtalk(url, secret, logger=logger)
        assert template_key in NOTIFY_TEMPLATE
        msg_body = deepcopy(NOTIFY_TEMPLATE[template_key]['template']['ding_work'])
        res = sender.send(msg_body, params=params, **kwargs)
        logger.debug(f"ding_robot message_status: {res}")


    @classmethod
    def _wechat(cls, aims: list, template_key, params: list, **kwargs):
        wx_info = kwargs['wx_info']
        wx_template = deepcopy(NOTIFY_TEMPLATE[template_key]["template"]['wechat'])
        wx_template['data'] = json.loads(wx_template['data'].format(*params))
        wx_template['template_id'] = wx_info['tpl_id']
        logger.info(wx_template)
        wechat_account = WechatPublicAccount(
            wx_info['app_id'],
            wx_info['app_secret']
        )
        for touser in aims:
            wx_template['touser'] = touser
            res = wechat_account.send_template_message(wx_template)
            logger.info(res)


    def notify(self, msg: dict):
        """
        向用户发送通知
        """
        logger.debug(f'got a msg:{msg}')
        # 公共参数
        method = msg['method']
        aims = msg['aims']
        params = msg["params"]
        template_key = msg['template_key']
        # 邮件和钉钉额外参数
        title_params = msg.get("title_params", [])
        # 微信额外参数
        wx_info = msg.get("wx_info", {})
        # 项目ID
        if not hasattr(self, f'_{method}'):
            logger.error(f'method={method} is invalid!')
            return
        # 项目ID
        project_id = msg["project_id"] if "project_id" in msg else None
        try:
            getattr(self, f'_{method}')(
                aims,
                template_key,
                params,
                title_params=title_params,
                wx_info=wx_info,
                project_id=project_id
            )
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(f'msg:{msg}, reason:{e}')


if __name__ == "__main__":
    while True:
        logger.info('notifier started.')
        try:
            notifier = Notifier()
            notify_mq =NotifierMq(callback=notifier.notify, logger=logger)
            notify_mq.wait_msg_blocked(concurrency=4)
        except Exception as e:
            logger.error(traceback.format_exc())

    # email_test
    # aims = ['v1150121351@126.com', ]
    # template_key = 'alarm_message'
    # params = ['device', 'rule', 'remark']
    # title_params = ['device']
    # Notifier()._email(aims, template_key, params, title_params)

    # msg = {
    #     'method': 'email',
    #     'aims': ['v1150121351@126.com'],
    #     'template_key': 'register_invite',
    #     'title_params': ['梁凯', 'EZtCloud', '周智鹏专用测试项目'],
    #     'params': ['梁凯', 'EZtCloud', '周智鹏专用测试项目', '邮箱', '邮箱', '39188043@qq.com',
    #                'https://api.isw.hotanzn.com', 'email', '39188043@qq.com'],
    #     'time': 1683785949493
    # }
    # # Notifier()._notify(msg)
