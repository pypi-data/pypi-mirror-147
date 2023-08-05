#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
Main module
"""
import logging
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

import urllib3

from . import auth
from . import constants
from . import settings
from . import station_client

# Init logger
formatter = logging.Formatter('%(asctime)s %(levelname)s %(process)d -- %(module)s#%(funcName)s : %(message)s')
rotating_file_handler = RotatingFileHandler(
    settings.log_file,
    maxBytes=settings.log_max_bytes,
    backupCount=settings.log_backup_count)
rotating_file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(rotating_file_handler)
if settings.log_include_console_handler:
    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
logger.setLevel(settings.log_level)

# Disable warnings about unsecure connection, since HTTPS verify is set to False due to self signed certificate.
urllib3.disable_warnings()

__all__ = [
    'constants',
    'settings',
    'auth',
    'station_client'
]
