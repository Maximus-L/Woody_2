# -*- coding: utf-8 -*-
import os
import re

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import Lib

CHUNK_SIZE = 2048
DEFAULT_PATH = './TMP'
log: Lib.AppLogger = Lib.AppLogger(__name__, 'BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.ERROR)


class InvalidUrlFile(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def url_is_valid(url) -> bool:
    """
    Проверяет, является ли 'url' действительным URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def url_download_file(url, destination_path=DEFAULT_PATH, verify=True) -> str | None:
    """
    :param destination_path:
    :param url: ссылка на файл для скачивания
    :param destination_path: путь куда скачивать
    :return: Имя загруженного файла | None - если не скачан
    """
    try:
        res = requests.get(url, verify=verify)
    except Exception as e:
        raise InvalidUrlFile(f'Файл:{url} невозможно загрузить ({e})')
    dest_file = os.path.join(os.path.abspath(destination_path),
                             os.path.basename(url))
    log.debug(dest_file)
    try:
        with open(dest_file, 'wb') as file:
            file.write(res.content)
        return dest_file
    except Exception as e:
        log.error(f'{dest_file} не может быть записан. {e}')
        return None


def url_download_long_file(url, destination_path=DEFAULT_PATH) -> str | None:
    """
    :param destination_path:
    :param url: ссылка на файл для скачивания
    :param destination_path: путь куда скачивать
    :return: Имя загруженного файла | None - если не скачан
    """
    try:
        res = requests.get(url)
    except Exception as e:
        raise InvalidUrlFile(f'Файл:{url} невозможно загрузить ({e})')
    dest_file = os.path.join(os.path.abspath(destination_path),
                             os.path.basename(url))
    log.debug(dest_file)
    try:
        with open(dest_file, 'wb') as file:
            for part in res.iter_content(CHUNK_SIZE):
                file.write(part)
        return dest_file
    except Exception as e:
        log.error(f'{dest_file} не может быть записан. {e}')
        return None


def url_get_content_js(url,
                       var_search='var RSMP_REGION = {(.+?)}'):
    """
    :param url: адрес страницы
    :param var_search: шаблон поиска
    :return: возвращает строку типа:
            'var RSMP_REGION = {"40":"Калуга", "71":"Тула"}'
    """
    if not url_is_valid(url):
        log.error(f'Invalid url: {url}')
        return None
    res = None
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    scripts = soup.findAll('script', {'type': "text/javascript"})
    for data in scripts:
        res1 = re.finditer(var_search, data.text)
        if res1 is not None:
            for res in res1:
                return res.group(0)
    return res
