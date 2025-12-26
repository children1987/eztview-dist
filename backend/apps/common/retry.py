# -*- coding: utf-8 -*-
import logging
import time
from functools import wraps


def retry(exception, tries=3, delay=1, back_off=1, logger=None):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exception as ex:
                    msg = "%s, Retrying in %d seconds..." % (str(ex), m_delay)
                    if logger:
                        logger.warning(msg)
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= back_off
            return str(ex)
        return f_retry
    return deco_retry


logging.basicConfig(level=logging.DEBUG)


@retry(Exception, logger=logging)
def retry_demo():
    # do sth.
    pass


if __name__ == "__main__":
    retry_demo()
