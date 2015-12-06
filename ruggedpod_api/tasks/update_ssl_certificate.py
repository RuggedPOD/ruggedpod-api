# RuggedPOD management API
#
# Copyright (C) 2015 Guillaume Giamarchi <guillaume.giamarchi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import time
import shutil

from celery.utils.log import get_task_logger
from ruggedpod_api.tasks import *

logger = get_task_logger(__name__)


@async.task()
def task(certificate, private_key):
    logger.info("SSL certificate is about to be updated")

    ssl_config = config.get_attr('authentication')['ssl']
    cert_file = ssl_config['certificate_file']
    private_key_file = ssl_config['private_key_file']

    logger.info("Backup the current SSL certificate")

    backup_template = "%s.backup"
    cert_file_backup = backup_template % cert_file
    private_key_file_backup = backup_template % private_key_file

    shutil.copy2(cert_file, cert_file_backup)
    shutil.copy2(private_key_file, private_key_file_backup)

    logger.info("Write new certificate")

    with open(cert_file, "w") as wfile:
        wfile.write(certificate)
    with open(private_key_file, "w") as wfile:
        wfile.write(private_key)

    logger.info("Reload web server configueation")
    status = os.system("service apache2 reload")

    if status != 0:
        logger.error("Apache reload did not succeed. Let's try to revert to the previous configuration")
        shutil.copy2(cert_file_backup, cert_file)
        shutil.copy2(private_key_file_backup, private_key_file)

        logger.info("Intentionally restart instead of a reaload to avoid unexpected weird side effects")
        status = os.system("service apache2 restart")
        if status != 0:
            logger.error("Revert configuration failed ! Don't know what to do")
            raise exception.RuggedpodException()
