# -*- coding: utf-8 -*-
__doc__ = """
Модуль содержит функцию обработки XML-файлов
load_xml_multiproc(q_files, q_res, spr_reg)
"""

import datetime as dt
import multiprocessing

from lxml import objectify
import pandas as pd

import Lib

COLUMNS = ['prizn', 'region_id', 'rep_date', 'inn', 'ogrn', 'okved1', 'okved', 'opf']
COLUMNS_STAFF = ['rep_date', 'inn', 'staff']

OPF_UL = 187  # Юридическое лицо
OPF_IP = 186  # Физическое лицо

# Группировка кодов ОКВЭД по отраслям. Группируется первая часть ОКВЭД.
# <Начало диапазона>, <конец диапазона>, <присваеваемый код>, <отрасль>
OKVED_GROUP = [
    [1, 3, 103, 'Сельское хозяйство'],
    [10, 33, 1033, 'Обрабатывающие производства'],
    [41, 43, 4143, 'Строительство'],
    [45, 47, 4547, 'Торговля'],
    [49, 53, 4953, 'Транспортировка и хранение'],
    [64, 66, 6466, 'Деятельность финансовая и страховая'],
    [68, 68, 6868, 'Операции с недвижимым имуществом'],
    [69, 75, 6975, 'деятельность профессиональная и научная'],
    [0, 0, 10000, 'Другое'],
    [4, 9, 10000, 'Другое'],
    [34, 40, 10000, 'Другое'],
    [44, 44, 10000, 'Другое'],
    [48, 48, 10000, 'Другое'],
    [54, 63, 10000, 'Другое'],
    [67, 67, 10000, 'Другое'],
    [76, 99, 10000, 'Другое']
]


log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   'BOTH',
                                   './LOGS/scaner.log',
                                   log_level=Lib.INFO)


def get_okved_dict():
    """
    Функция создает словарь из диапазонов OKVED_GROUP для подстановки кода группировки
    по отраслям.
    :return: словарь
    """
    range_okved = []
    range_group = []
    for gr in OKVED_GROUP:
        rng = range(gr[0], gr[1]+1)
        okv_id = gr[2]
        list_okved = [i1 for i1 in rng]
        list_group = [okv_id for _ in rng]
        range_okved = range_okved + list_okved
        range_group = range_group + list_group
    result = dict(zip(range_okved, range_group))
    return result


def load_xml_multiproc(q_files: multiprocessing.JoinableQueue,
                       q_res: multiprocessing.JoinableQueue,
                       spr_reg: dict):
    """
    Функция обработки XML-файлов по МСП - ИП и ЮЛ, полученным с сайта nalog.ru
    Запуск производится с использованием встроенной библиотеки multiprocessing
    Имена обрабатываемых файлов извлекаются из очереди, обработанные данные
    помещаются в датафрейм (библиотека pandas), датафрейм добавляется в очередь
    для последующей обработки
    :param q_files: очередь имен XML-файлов
    :param q_res: очередь датафреймов, полученных в результате обработки XML
    :param spr_reg: словарь соответствий кодов регионов и ID регионов из БД
    :return: ---------
    """
    cur_proc_name = multiprocessing.current_process().name
    okv_gr = get_okved_dict()
    # пока в очереди есть файлы
    while not q_files.empty():
        # извлечение имени файла
        fname = q_files.get()
        files_to_job = q_files.qsize()
        # разбор файла
        xml = objectify.parse(fname)
        root = xml.getroot()
        # извлечение дочерних ветвей
        ch_docs = root.getchildren()
        i, i_err = 0, 0  # счетчик обработанных записей, счетчик ошибочных
        # инициализация датафрейма
        res = pd.DataFrame(columns=COLUMNS)
        for one_doc in ch_docs:
            if one_doc.tag == 'Документ':
                try:
                    # извлечение параметров по каждому ИП, ЮЛ
                    region1 = int(one_doc.СведМН.get('КодРегион'))
                    region = spr_reg[region1]
                    rep_date = dt.datetime.strptime(one_doc.get('ДатаСост'), '%d.%m.%Y')
                    f_new = 0
                    rep_date = dt.date(rep_date.year, rep_date.month, 1)
                    onne_doc_child = one_doc.getchildren()
                    ogrn = 0
                    # в зависимости от типа организации (ИП или ЮЛ):
                    if 'ИПВклМСП' in [a.tag for a in onne_doc_child]:
                        inn = int(one_doc.ИПВклМСП.get('ИННФЛ'))
                        opf = OPF_IP
                        staff = None
                    elif 'ОргВклМСП' in [a.tag for a in onne_doc_child]:
                        inn = int(one_doc.ОргВклМСП.get('ИННЮЛ'))
                        opf = OPF_UL
                        staff = one_doc.get('ССЧР')
                    else:
                        inn = None
                        ogrn = None
                        opf = None
                        staff = None
                    okved = '00.00'
                    try:
                        okved = one_doc.СвОКВЭД.СвОКВЭДОсн.get('КодОКВЭД')
                    except Exception:
                        i_err += 1
                    finally:
                        okved_a = okved.split('.')
                        okved1 = okv_gr[int(okved_a[0])]
                    i += 1
                    # добавление строки в датафрейм
                    res = pd.concat([res,
                                     pd.DataFrame([[f_new, region, rep_date, inn, ogrn,
                                                    okved1, okved, opf]],
                                                  columns=COLUMNS)])
                except Exception as e:
                    i_err += 1
                    print(e)
        # датафрейм помещается в очередь с результатами обработки
        q_res.put(res)
        # сигнал об обработке очередного элемента очереди
        q_files.task_done()
        # логирование количества обработанных записей из XML-файла
        log.info(f'Загружено:{i}; ошибочных:{i_err} ({cur_proc_name})[осталось {files_to_job}]')


def load_xml_staff(q_files: multiprocessing.JoinableQueue,
                   q_res: multiprocessing.JoinableQueue):
    """
    Функция обработки XML-файлов по количеству работников МСП, полученным с сайта nalog.ru
    Имена обрабатываемых файлов извлекаются из очереди, обработанные данные
    помещаются в датафрейм (библиотека pandas), датафрейм добавляется в очередь
    для последующей обработки
    :param q_files: очередь имен XML-файлов
    :param q_res: очередь датафреймов, полученных в результате обработки XML
    :return: ---------
    """
    one_day = dt.timedelta(days=1)
    # пока в очереди есть файлы
    while not q_files.empty():
        # извлечение имени файла
        fname = q_files.get()
        files_to_job = q_files.qsize()
        # разбор файла
        xml = objectify.parse(fname)
        root = xml.getroot()
        # извлечение дочерних ветвей
        ch_docs = root.getchildren()
        i, i_err = 0, 0  # счетчик обработанных записей, счетчик ошибочных
        # инициализация датафрейма
        res = pd.DataFrame(columns=COLUMNS_STAFF)
        for one_doc in ch_docs:
            if one_doc.tag == 'Документ':
                try:
                    # извлечение параметров по каждому ЮЛ
                    inn = one_doc.СведНП.get('ИННЮЛ')
                    staff = int(one_doc.СведССЧР.get('КолРаб'))
                    rep_date = dt.datetime.strptime(one_doc.get('ДатаСост'), '%d.%m.%Y')+one_day
                    rep_date = dt.date(rep_date.year, rep_date.month, 1)
                    i += 1
                    # добавление строки в датафрейм
                    res = pd.concat([res,
                                     pd.DataFrame([[rep_date, inn, staff]],
                                                  columns=COLUMNS_STAFF)])
                except Exception as e:
                    i_err += 1
                    print(e)
        # датафрейм помещается в очередь с результатами обработки
        q_res.put(res)
        # сигнал об обработке очередного элемента очереди
        q_files.task_done()
        # логирование количества обработанных записей из XML-файла
        log.info(f'Загружено:{i}; ошибочных:{i_err} [осталось {files_to_job}]')
