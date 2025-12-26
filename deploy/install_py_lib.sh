#!/bin/bash

echo -e "请输入第三方库和版本号，例：xxxx==0.94.1 \n"
read choice
echo -e "\n"
echo -e "请输入指定源URL，默认豆瓣源，如不指定，直接按回车跳过 \n"
read URL


if [ -n "$URL" ]; then
    install_command="pip install $choice -i $URL"
else
    install_command="pip install $choice -i https://pypi.doubanio.com/simple/"
fi


container_list=("mcq_web_server" "mcq_celery" "mcq_celery_beat" "mcq_device_monitor" "mcq_isw_adapter" "mcq_wechat_pay_server")

for container in "${container_list[@]}"
do
    docker exec $container $install_command
done
