# -*- coding: utf-8 -*-
__doc__ = """
Модуль загрузки из эксель и формирование результирующего датафрейма
    Функция работы с XLS-файлами, содержащими данные в формате:
    -------------------------------------------
    |РЕГИОН ИМЯ   |Дата 1|Дата 2|......|Дата n|
    -------------------------------------------
    |Россия       |   112|   45 |......|      |
    -------------------------------------------
    Калужская обл |   23 |   4  |......|      |
    -------------------------------------------
    Именам регионов ставятся в соответствие коды регионов, даты преобразуются
    согласно маске. Даты могут встречаться в разном формате:
    "01.12.2021" "12/25/2021" "Август 2021"
    на выходе формируется Pandas Dataframe вида:
    [OKATO_ID, DATE_, VALUE]
"""

import os.path
import re
import datetime as dt
import locale

import pandas as pd

import Lib
import Scaner.const as const

# А вот это исключительно для того, чтобы "Август 2021" правильно конвертился
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
log: Lib.AppLogger = Lib.AppLogger(__name__, output='BOTH',
                                   log_file='./LOGS/scan.log')

DEFAULT_FILE = '1.xlsx'
ENGINE10 = 'x'
DEFAULT_SHEET_NAME = 'Лист1'
DEFAULT_DATE_RE = '\d{,2}/\d{,2}/\d{4}'
DEFAULT_DATE_FORMAT = '%m/%d/%Y'
DEFAULT_REGION_SUFFIX = ' (по методологии)'
RES_COLUMN = ['VAL_ID', 'OKATO_ID', 'DATE_', 'VALUE']


def xls_reader_date_column(
        file_name: str = 'default.xlsx',
        sheet_name: str = 'sheet1',
        val_id: int = 0,
        header: int = 0,
        region_name_col: str = 'Unnamed: 0',
        region_id_col: str = 'Unnamed: 1',
        region_suffix: str = DEFAULT_REGION_SUFFIX,
        date_re: str = DEFAULT_DATE_RE,
        date_format: str = DEFAULT_DATE_FORMAT,
        spr: Lib.Spr = None,
        return_last_date: bool = True
) -> [dt.datetime | None, pd.DataFrame | None]:
    """
    Параметры:
        file_name   имя файла эксель,
        val_id      id показателя
        header      номер строки с заголовками,
        region_name_col имя столбца с наименованием регионов
                        (может быть без имени, тогда "Unnamed: 1"),
        region_id_col   имя столбца с кодами регионов, если не существует будет создан,
        region_suffix   суффикс в имени региона, который надо удалить,
        date_re         регул.выраж. для поиска в наименованиях столбцов даты,
        date_format     формат преобразования даты,
        spr: applib.Spr экземпляр справочника регионов
        :rtype: object
    """
    max_date = None
    # результирующий датафрейм
    res = pd.DataFrame(columns=RES_COLUMN)
    try:
        # чтение эксель файла в датафрейм
        if os.path.splitext(file_name)[1].upper() == '.XLSX':
            engine = 'openpyxl'
        else:
            engine = 'xlrd'
        x = pd.read_excel(file_name,
                          sheet_name=sheet_name,
                          header=header,
                          engine='openpyxl')
    except Exception as e:
        log.error(f'Файл {file_name} не найден! {e}')
        return False
    # формирование списка имен столбцов загруженного датафрейма
    list_col_names = x.columns.to_list()
    # проверка корректности имени столбца с именами регионов
    if region_name_col in list_col_names:
        # удаление суффикса из имен регионов
        x[region_name_col] = x[region_name_col].apply(lambda y: y.rsplit(region_suffix, 1)[0])
        # формирование столбца с кодами регионов
        x[region_id_col] = x[region_name_col].apply(spr.find_by_key)
        # удаление строк, для которых не найден код региона
        x = x.dropna(subset=[region_id_col])
    else:
        log.error(f'Не найден {region_name_col}')
        return [None, None]
    for col in list_col_names:  # перебор всех колонок во входном датафрейме
        # если имя столбца содержит дату (поиск по регулярке)
        if type(col) is dt.datetime:
            date = col
        elif re.search(date_re, col) is not None:
            # конвертирование имени столбца в дату
            date = dt.datetime.strptime(col, date_format)
        else:
            date = None
        if date:
            if max_date is None or max_date < date:
                max_date = date
            # формирование промежуточного датафрейма - делается срез
            # состоящий из кода региона и значений, взятых из столбца
            # с конкретной датой
            res1 = pd.DataFrame(x[[region_id_col, col]])
            # переименование столбцов
            res1 = res1.rename(columns={region_id_col: RES_COLUMN[1],
                                        col: RES_COLUMN[3]})
            # добавление столбца с датой и id показателя
            res1[RES_COLUMN[2]] = date
            res1[RES_COLUMN[0]] = val_id
            # конкатенация результирующего и промежуточного датафрейма
            if res:
                res = pd.concat([res, res1])
            else:
                res = res1.copy(deep=True)
    return [max_date,
            res.loc[res[RES_COLUMN[2]] == max_date if return_last_date else res]]
# ----------------------------------------------------------------------------------------
