#!/bin/bash

#指定日志文件夹路径
LOG_DIR="/workspace/nginx/log"

#获取当前日期
CURRENT_DATE=$(date "+%Y-%m-%d")
#计算3天前的日期
OLD_DATE=$(date -d "3 days ago" "+%Y-%m-%d")
# 遍历日志文件夹
for logfile in "$LOG_DIR"/*; do
    # 提取文件名中的日期
    filename=$(basename "$logfile")
    filedate=${filename#nginx-access-}
    filedate=${filedate%.log}

    # 如果文件日期早于OLD_DATE,则删除文件
    if [[ "$filedate" < "$OLD_DATE" ]]; then
        rm "$logfile"
    fi
done
