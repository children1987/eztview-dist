#!/bin/sh
set -eu

# 1) 先重启 web_server
echo "[mcq-restart] restarting mcq_web_server ..."
docker restart mcq_web_server

# 2) 显式执行 migrate（幂等保险）
#    说明：mcq_web_server 在容器启动命令中已执行过一次 migrate；
#    这里再执行一遍用于防守式兜底（未来启动命令变更或异常启动路径），
#    且 migrate 幂等，重复执行不会重复应用迁移。
echo "[mcq-restart] running django migrate ..."
docker exec mcq_web_server sh -c "cd /workspace/mcq/backend && python manage.py migrate"

# 3) 再重启依赖数据库结构的其他服务
echo "[mcq-restart] restarting dependent services ..."
docker restart \
    mcq_celery \
    mcq_celery_beat \
    mcq_isw_adapter \
    mcq_wechat_pay_server \
    mcq_notifier \
    mcq_device_monitor

echo "[mcq-restart] done"
