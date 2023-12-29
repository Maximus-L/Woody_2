# -*- coding: utf-8 -*-

import os

import Lib

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.ERROR)


def clear_dir(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            log.error(f'Ошибка удаления: {file_path}. {e}')
