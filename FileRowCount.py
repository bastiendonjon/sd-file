"""
  Server Density Plugin
  File

  https://github.com/bastiendonjon/sd-file/

  Version: 1.0.0
"""

import json
import logging
import os
import platform
import sys
import time

class FileRowCount(object):

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()
        self.filesPath = self.raw_config['FileRowCount'].get('paths', '')

    def run(self):

        data = {}

        for filePath in self.filesPath.split(','):
            with open(filePath) as f:
                data[filePath] = sum(1 for _ in f)

        return data


if __name__ == '__main__':
    """Standalone test
    """

    raw_agent_config = {
        'FileRowCount': {
            'filesPath': '/var/tmp/myapp.log'
        }
    }

    main_checks_logger = logging.getLogger('File')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    file_check = File({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(file_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
