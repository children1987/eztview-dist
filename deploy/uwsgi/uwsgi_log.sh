#!/bin/bash
# 定义日志目录
LOG_DIR="/workspace/mcq/backend/log"

# 获取昨天的日期，格式为"年-月-日"
DATE=`date -d "yesterday" +"%Y-%m-%d"`

# 移动日志文件并创建备份
mv ${LOG_DIR}/uwsgi.log  ${LOG_DIR}/uwsgi_${DATE}.log

# 触发日志轮转的"占位"文件
touch /workspace/mcq/backend/log/.touchforlogrotat

# 设定保留的日志文件数量
number=3

# 获取最新日志文件（即最旧的备份日志），准备删除它
delfile=`ls -l -crt  $LOG_DIR/uwsgi_*.log | awk '{print $9 }' | head -1`

# 统计日志文件数量
count=`ls -l -crt  $LOG_DIR/uwsgi_*.log | awk '{print $9 }' | wc -l`

# 如果备份日志数量超过设定值，则删除最早生成的备份
if [ $count -gt $number ]
then
  rm $delfile
fi
