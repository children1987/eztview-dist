#!/bin/sh
docker restart \
    mcq_web_server \
    mcq_celery \
    mcq_celery_beat \
    mcq_isw_adapter \
    mcq_wechat_pay_server\
    mcq_notifier\
    mcq_device_monitor
