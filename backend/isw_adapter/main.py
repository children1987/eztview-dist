import traceback
import _setup_django
from backend.isw_adapter.isw_adapter_config import ISW_LOGGER
from backend.isw_adapter.up_server import IswUpServe

logger = ISW_LOGGER


def main():
    IswUpServe().run()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        logger.error('isw adapter 服务启动失败！')
        logger.error(err)
        logger.error(traceback.format_exc())
