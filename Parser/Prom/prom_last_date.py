# -*- coding: utf-8 -*-
import os.path
import re
import datetime as dt
from time import sleep

import requests
from bs4 import BeautifulSoup

import Parser.Urls

import pandas as pd

import Parser.XLS
import Scaner.const as const
import Lib.Spr

# CERT_MINC = '/usr/local/share/ca-certificates/russian-trusted/minc.crt'
# CERT_MINC = './SPR/minc.crt'
CERT_MINC = const.DATA_SOURCE['PROM']['ssl-cert']


log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   'BOTH',
                                   './LOGS/scaner.log',
                                   log_level=Lib.INFO)


class InvalidUrl(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def prom_last_date(url,
                  fdate_re='[P|p]rom_\d{,2}[_|-]\d{4}',
                  fdate_format='%m-%Y-%d'):
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
        print(url)
        with requests.Session() as s:
            s.verify = CERT_MINC
            try_count = 1
            while try_count<10:
                r = s.get(url, timeout=5)
                r = s.get(url, timeout=5)
                if r.status_code == 200: break
                try_count += 1
            if r.status_code != 200:
                raise InvalidUrl(url)
            soup = BeautifulSoup(r.content, 'html.parser')
    except Exception:
        return None
    url_server = url[:re.search('.ru', url).regs[0][1]]
    max_date = None  # максимальная дата файла
    url_for_load = None  # ссылка на файл
    # перебор всех ссылок
    links = soup.find_all('a')
    for link in links:   #soup.findAll("a"):
        # print(link.get('href'))
        file_ref = link.get('href')
        if file_ref is not None:
            # проверка наличия даты в имени файла (ссылки)
            # print(file_ref)
            data = re.search(fdate_re, file_ref)
            if data is not None:
                try:
                    # извлечение даты, проверка на "свежесть"
                    # print(data.group(0), file_ref)
                    sdate = data.group(0).replace('_', '-')+'-01'
                    date = dt.datetime.strptime(sdate[-10:], fdate_format)
                    date = dt.date(date.year, date.month, 1)
                    # print(date)
                    if max_date is None or date > max_date:
                        max_date = date
                        url_for_load = url_server + file_ref.strip()
                        print(url_for_load)
                except Exception as e:
                    log.error(f'Дата не в формате. {e}')
    return list([max_date, url_for_load])


def prom_data(url: str) -> pd.DataFrame | None:
    name = 'PROM'
    qparams = {"downloadformat": "xlsx"}
    fname = Parser.Urls.url_download_file(url,
                                          os.path.join( const.DATA_SOURCE[name]['store_path'], 'TMP'),
                                          verify=CERT_MINC,
                                          qparams=qparams)
    x = pd.read_excel(fname,
                      sheet_name=const.DATA_SOURCE[name]['values'],
                      header=const.DATA_SOURCE[name]['header'],
                      engine='openpyxl')
    first_row = x.loc[x[const.DATA_SOURCE[name]['filter_col']] == const.DATA_SOURCE[name]['filter_begin']].index[0]
    last_row = x.loc[x[const.DATA_SOURCE[name]['filter_col']] == const.DATA_SOURCE[name]['filter_end']].index[0]
    result = x[first_row:last_row]
    return result
