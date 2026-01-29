#!/bin/sh
# 本文件用于重新部署后端服务
project_name="mcq"

# 固定到 deploy 目录运行，避免相对路径导致找不到文件
cd /workspace/mcq/deploy || exit 1

echo "git configging ..."
git config core.filemode false
echo "git configging finished. "

echo "git pull 开始"
cd /workspace/mcq || exit 1
git pull
chmod +x auto_deploy*.sh 2>/dev/null || true
cd /workspace/mcq/deploy || exit 1
echo "git pull 完成"

echo "注意：请确保前端打包已完成"

# 配置nginx
nginx_cfg_file_name=$project_name"_nginx.conf"
if [ ! -f "/workspace/nginx/projects/$nginx_cfg_file_name" ]; then
    echo "copy Nginx config file"
    mkdir -p /workspace/nginx/projects

    echo "copy ./nginx/"$nginx_cfg_file_name" to /workspace/nginx/projects/"
    cp ./nginx/$nginx_cfg_file_name /workspace/nginx/projects/

    echo "docker restart nginx"
    docker restart nginx
fi

# 关键改动：mcq:latest 只构建一次，避免 docker-compose 对同一个 tag 并行 build 导致冲突
echo "docker build mcq:latest ..."
docker build -t mcq:latest -f /workspace/mcq/deploy/Dockerfile /workspace/mcq

# 不再执行 docker-compose build，直接 up（会复用本地 mcq:latest）
echo "docker-compose up -d ..."
docker-compose -p $project_name up -d
echo "docker-compose up -d finished."

# add 定时任务
if [ `crontab -l | grep -c mcq` -eq 0 ];then
  crontab -l > old_crontab.backup
  echo "添加 cron task"
  (crontab -l ; echo "0 0 * * * sh /workspace/mcq/deploy/uwsgi/uwsgi_log.sh") | crontab
  (crontab -l ; echo "0 0 * * * sh /workspace/mcq/deploy/nginx/rm-nginxlog.sh") | crontab
  (crontab -l ; echo "*/20 * * * * docker exec -i mcq_web_server python /workspace/mcq/backend/device_monitor/server_data_checker.py >> /workspace/mcq/backend/log/server_data_checker.out 2>&1") | crontab
else
  echo 'cron tasks 已存在'
fi
