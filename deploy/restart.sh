#!/bin/sh
set -eu

# 先串行执行一次 migrate，避免与 web_server 启动命令内 migrate 并发
# （web_server command 中也会执行 migrate，这里先完成可把并发风险降为 0）
echo "[mcq-restart] running django migrate (one-off container) ..."
docker-compose -p mcq run --rm --no-deps mcq_web_server \
    sh -c "cd /workspace/mcq/backend && python manage.py migrate"

# 再重启 web_server
echo "[mcq-restart] restarting mcq_web_server ..."
docker restart mcq_web_server

# 最后重启依赖数据库结构的其他服务
echo "[mcq-restart] restarting dependent services ..."
docker restart \
    mcq_celery \
    mcq_celery_beat \
    mcq_isw_adapter \
    mcq_wechat_pay_server \
    mcq_notifier \
    mcq_device_monitor

echo "[mcq-restart] done"
