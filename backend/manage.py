#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # 项目根目录（backend 的上级目录）
    # 使用 Path(__file__).resolve() 确保始终得到绝对路径，兼容所有导入方式
    current_path = Path(__file__).resolve().parent  # backend 目录
    proj_root = current_path.parent  # 项目根目录
    sys.path.insert(0, str(proj_root))
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings.base")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    execute_from_command_line(sys.argv)
