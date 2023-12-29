# -*- coding: utf-8 -*-

import re
import datetime as dt

import requests
from bs4 import BeautifulSoup

import Lib
import Parser.Urls

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   'BOTH',
                                   './LOGS/scaner.log',
                                   log_level=Lib.INFO)


class InvalidUrl(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def msp_last_date(url,
                  fdate_re='data-\d{8}-',
                  fdate_format='data-%d%m%Y-'):
    """
    :param url: ссылка для поиска файлов
    :param fdate_re: маска для поиска файлов
    :param fdate_format: формат даты в имени файла
    :return: список, [0] - дата самого свежего файла
                    [1] - ссылка на этот файл
    """
    if not Parser.Urls.url_is_valid(url):
        raise InvalidUrl(url)
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
    except Exception:
        return None
    max_date = None  # максимальная дата файла
    url_for_load = None  # ссылка на файл
    # перебор всех ссылок
    for link in soup.findAll("a"):
        file_ref = link.get('href')
        if file_ref is not None:
            # проверка наличия даты в имени файла (ссылки)
            data = re.search(fdate_re, file_ref)
            if data is not None:
                try:
                    # извлечение даты, проверка на "свежесть"
                    date = dt.datetime.strptime(data.group(0), fdate_format)
                    date = dt.date(date.year, date.month, 1)
                    if max_date is None or date > max_date:
                        max_date = date
                        url_for_load = file_ref.strip()
                except Exception as e:
                    log.error(f'Дата не в формате. {e}')
    return list([max_date, url_for_load])
