# -*- coding: utf-8 -*-

import Parser.Urls
import Lib

log: Lib.AppLogger = Lib.AppLogger(__name__, output='BOTH',
                                   log_file='./LOGS/scaner.log')


def download_arc(name, url, dest_path) -> str | None:
    if name == 'MSP':
        try:
            file_name = Parser.Urls.url_download_long_file(url,
                                                           destination_path=dest_path)
            return file_name
        except Exception as e:
            log.error(f'Файл не загружен: {url}, {e}')
            return None
