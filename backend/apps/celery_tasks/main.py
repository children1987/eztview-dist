# -*- coding: utf-8 -*-
import django
import sys
import os
from pathlib import Path

from celery import Celery

# 项目根目录（backend 的上级目录）
# 使用 Path(__file__).resolve() 确保始终得到绝对路径，兼容所有导入方式
SCRIPT_DIR = Path(__file__).resolve().parent  # backend/apps/celery_tasks
APPS_DIR = SCRIPT_DIR.parent  # backend/apps
BASE_DIR = APPS_DIR.parent  # backend
PROJ_ROOT = BASE_DIR.parent  # 项目根目录
sys.path.insert(0, str(PROJ_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings.base")
django.setup()

from django.conf import settings

celery_app = Celery(settings.PROJ_NAME)

# 导入配置文件
celery_app.config_from_object('backend.apps.celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks([
    'backend.apps.celery_tasks.air_servers_tasks',
    'backend.apps.celery_tasks.device_tasks',
    'backend.apps.celery_tasks.ew_statistics_tasks',
    'backend.apps.celery_tasks.el_prepayment_tasks',
])

# 开启celery的命令
#  celery -A 应用路径（.包路径） worker -l info
#  celery -A celery_tasks.main worker -l debug
#  celery multi start w1 -A celery_tasks.main -l info      #  linux启动命令
#  celery multi restart w1 -A celery_tasks.main -l info    # linux重启命令
#  celery -A celery_tasks.main worker -l info --pool=solo  # windows本地调试命令
#  celery -A celery_tasks.main beat -l info  # 定时任务启动
#  celery -A celery_tasks.main beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
