import traceback
import _setup_django

from backend.device_monitor.config import device_monitor_logger as logger
from backend.device_monitor.state_checker import DeviceStateChecker
from backend.m_common.debugger import rerun


@rerun(
    'DeviceStateChecker 在线轮询检测器重启中',
    logger=logger,
    max_retry_count=3
)
def device_state_check_task():
    checker = DeviceStateChecker()
    checker.run()


if __name__ == '__main__':
    try:
        device_state_check_task()
    except Exception as err:
        logger.error('Device Monitor 服务启动失败！')
        logger.error(err)
        logger.error(traceback.format_exc())
