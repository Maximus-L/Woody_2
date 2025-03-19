# -*- coding: utf-8 -*-

import multiprocessing
import fnmatch
import time
from pathlib import Path
import os

# advanced libs
# import pandas as pd

# self libs
import Lib
import Parser.MSP

PROC_XML = 10
PATH_XML_TMP = './TEMP'
PATH_XML_CSV = './CSV_MSP'
q_files = multiprocessing.JoinableQueue()
q_res = multiprocessing.JoinableQueue()

log: Lib.AppLogger = Lib.AppLogger(__name__, 'BOTH', log_file='./LOGS/msp.log')


def q_files_fill(input_path):
    """
    Заполняет очередь q_files именами XML-файлов с полным путем
    :param input_path: стартовый путь для поиска XML-файлов
    :return:
    """
    full_path = os.path.abspath(input_path)
    for rootkit, subdir, filenames in os.walk(full_path):
        for filename in fnmatch.filter(filenames, '*.xml'):
            full_name = Path(rootkit) / filename
            q_files.put(full_name)


def save_res_csv(q_res: multiprocessing.JoinableQueue,
                 output_file):
    """
    Функция извлекает из очереди q_res датафреймы и записывает
    их в файл, указанный в параметре output_file
    :param q_res: очередь с датафреймами
    :param output_file: путь и имя файла CSV
    """
    j = 0
    while not q_res.empty():
        df = q_res.get()
        df.to_csv(output_file,
                  sep=';',
                  mode='a' if j > 0 else 'w',
                  index=False,
                  header=j == 0)
        j += 1


def parse_xml_msp_2csv(xml_dir=PATH_XML_TMP,
                       csv_file=os.path.join(PATH_XML_CSV, '1.csv'),
                       spr_regions: Lib.Spr = None):
    # инициализация параметров получаемых из командной строки
    t0 = time.perf_counter()  # для подсчета времени выполнения
    # заполнение очереди именами обрабатываемых XML-файлов
    q_files_fill(xml_dir)
    files_count = q_files.qsize()
    for i in range(PROC_XML):
        # инициализация процессов
        p = multiprocessing.Process(target=Parser.MSP.load_xml_multiproc,
                                    name='XML_ldr_' + str(i + 1),
                                    args=(q_files, q_res, spr_regions.values))
        p.start()
    q_files.join()
    t1 = time.perf_counter()
    t = int(t1 - t0)
    # вывод времени обработки XML-файлов
    log.info(f'Обработано {files_count} файлов за {t // 60:02d}:{t % 60:02d}')
    # сохранение результатов в CSV-файле либо в БД
    save_res_csv(q_res, csv_file)
    while not q_res.empty():
        a = q_res.get()


def parse_xml_staff_2csv(xml_dir=PATH_XML_TMP,
                         csv_file=os.path.join(PATH_XML_CSV, '1.csv')):
    # инициализация параметров получаемых из командной строки
    t0 = time.perf_counter()  # для подсчета времени выполнения
    # заполнение очереди именами обрабатываемых XML-файлов
    q_files_fill(xml_dir)
    files_count = q_files.qsize()
    Parser.MSP.load_xml_staff(q_files, q_res)
    t1 = time.perf_counter()
    t = int(t1 - t0)
    # вывод времени обработки XML-файлов
    log.info(f'Обработано {files_count} файлов за {t // 60:02d}:{t % 60:02d}')
    # сохранение результатов в CSV-файле либо в БД
    save_res_csv(q_res, csv_file)
