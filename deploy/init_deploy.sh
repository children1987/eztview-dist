#!/bin/sh
# 本文件用于重新部署后端服务
project_name="mcq"

echo "git configging ..."
git config core.filemode false
echo "git configging finished. "

echo "git pull 开始"
git pull
chmod +x auto_deploy*.sh
echo "git pull 完成"

# 前端静态文件生成
# 方式1: 适用于服务器本地存放
# echo "本地前端打包 开始"
# docker run -it --rm --name mycnpm --network host -v /workspace/$project_name:/workspace/$project_name -w /workspace/$project_name/frontend_web_v5 children1987/mycnpm:12-alpine cnpm i
# docker run -it --rm --name mycnpm --network host -v /workspace/$project_name:/workspace/$project_name -w /workspace/$project_name/frontend_web_v5 children1987/mycnpm:12-alpine cnpm run build
# echo "本地前端打包 完成"
# 方式2: 适用于cos存放
echo "注意：请确保前端打包已完成"

# 配置nginx
nginx_cfg_file_name=$project_name"_nginx.conf"
# echo "remove old Nginx config file"
# rm -f /workspace/nginx/projects/$nginx_cfg_file_name
if [ ! -f "/workspace/nginx/projects/$nginx_cfg_file_name" ]; then
    echo "copy Nginx config file"
    mkdir -p /workspace/nginx/projects

    echo "copy ./nginx/"$nginx_cfg_file_name" to /workspace/nginx/projects/"
    cp ./nginx/$nginx_cfg_file_name /workspace/nginx/projects/

    echo "docker restart nginx"
    docker restart nginx
fi

echo "docker-compose build ..."
docker-compose build

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
