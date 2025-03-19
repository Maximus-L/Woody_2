# -*- coding: utf-8 -*-
import os
import zipfile

import Lib
import Lib.Files

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.ERROR)


class InvalidPath(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def unzip_file(file_name, dest_path='./TEMP'):
    """
    :param file_name: файл для распаковки
    :param dest_path: путь куда распаковывать
    :return: None
    """
    Lib.Files.clear_dir(dest_path)
    if zipfile.is_zipfile(file_name):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(dest_path)
    else:
        log.error(f'File {file_name} is not ZIP')


def zip_file(src_file, zip_file_name):
    if os.path.isfile(src_file):
        with zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip_ref:
            zip_ref.write(src_file,
                          arcname=os.path.basename(src_file),
                          compress_type=zipfile.ZIP_DEFLATED,
                          compresslevel=9)
    else:
        log.error(f'Файл не найден: {src_file}')
