# -*- coding: utf-8 -*-

import Parser.Urls

import datetime as dt
import re
import ast
from typing import Any
import pandas as pd
from pandas import DataFrame, Series

import Lib

RE_REGION = 'var RSMP_REGION = {(.+?)}'
RE_DATA_BUSY = 'var STATISTICS_DATA = \\[(.+?)\\]'
BUSY_DATE_FORMAT = '%d.%m.%Y'
# префиксы ключей в словарях
VAL_PREFIX = ['cnt_', 'cnt_worker_']
# суффиксы ключей в словарях - организационно-правовая форма:
#           всего      ЮЛ          ИП
VAL_OPF = {'': 190, 'ul_': 187, 'ip_': 186}
# Категории МСП:   всего       микро      мини        средние
VAL_CATEGORY = {'total': 5, 'micro': 6, 'mini': 3, 'normal': 4}
# ключ даты
DATE_KEY = 'stat_date'
# ключ регион
REGION_KEY = 'cnt_name'
# столбцы в результирующем датафрейме
COLUMNS = ['date', 'region', 'opf', 'cat', 'factory', 'staff']
# COLUMNS = ['date', 'region', 'opf', 'cat', 'factory', 'staff', 'tst_r']

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.ERROR)


def busy_last_date(url, spr_regions: Lib.Spr = None) -> list[DataFrame | Series | None | Any]:
    """
    :param url: адрес страницы реестра МСП по занятым
    :param spr_regions: объект справочник регионов
    :return: [0] - дата данных
             [1] - датафрейм с набором данных
    """
    date, reg_id = None, None
    # результирующий датафрейм
    result = pd.DataFrame(columns=COLUMNS, index=None)
    try:
        # считывание со страницы реестра МСП и выделение нужных данных
        all_data = Parser.Urls.url_get_content_js(url, var_search=RE_DATA_BUSY)
    except Exception as e:
        raise e
    # Разделение строки со словарями на список строк, в каждой - 1 словарь
    str_dicts = re.finditer("{(.+?)}", all_data)
    # Цикл по списку строк со словарями
    for str_dict in str_dicts:
        # Преобразование строки со словарем в словарь
        reg_dict = ast.literal_eval(str_dict.group(0))
        # Дата
        date_str = reg_dict[DATE_KEY][0:10] if DATE_KEY in reg_dict else None
        # Регион
        region = reg_dict[REGION_KEY] if REGION_KEY in reg_dict else None
        # Перевод строки с датой в объект datetime
        date = dt.datetime.strptime(date_str, BUSY_DATE_FORMAT)
        date = dt.date(date.year, date.month, 1)
        # Поиск в справочнике кода региона для загрузки в БД
        if spr_regions is not None:
            reg_id = spr_regions.find_by_key(region)
        else:
            reg_id = None
        # Цикл по категориям
        for v_cat in list(VAL_CATEGORY.keys()):
            cat = VAL_CATEGORY[v_cat]
            # Цикл по ОПФ
            for v_opf in list(VAL_OPF.keys()):
                opf = VAL_OPF[v_opf]
                # формирование ключа
                factory_key_val = VAL_PREFIX[0] + v_opf + v_cat
                staff_key_val = VAL_PREFIX[1] + v_opf + v_cat
                # по сформированному ключу извлечение данных
                if factory_key_val in reg_dict:
                    factory = reg_dict[factory_key_val]
                else:
                    # Отсутствует ключ в данных cnt_total cnt_micro ...
                    # поэтому "всего" по ОПФ получаем суммированием ЮЛ + ИП
                    factory = 0
                    for k1 in list(VAL_OPF.keys()):
                        k2 = VAL_PREFIX[0] + k1 + v_cat
                        factory = factory + int(reg_dict[k2]) if k1 != '' else 0

                if staff_key_val in reg_dict:
                    staff = reg_dict[staff_key_val]
                else:
                    # Отсутствует ключ в данных cnt_total cnt_micro ...
                    # поэтому "всего" по ОПФ получаем суммированием ЮЛ + ИП
                    staff = 0
                    for k1 in list(VAL_OPF.keys()):
                        k2 = VAL_PREFIX[1] + k1 + v_cat
                        staff = staff + int(reg_dict[k2]) if k1 != '' else 0

                # factory = reg_dict[factory_key_val] if factory_key_val in reg_dict else None
                # staff = reg_dict[staff_key_val] if staff_key_val in reg_dict else None
                result = pd.concat([result,
                                    pd.DataFrame([[date, reg_id, opf, cat, factory, staff]],
                                                 columns=COLUMNS)
                                    ], ignore_index=True)
    return list([date, result])
