# -*- coding: utf-8 -*-
import csv
import os
import pathlib
from typing import Any

import openpyxl

import Lib

SPR_SOURCE_XLS = '.XLSX'   # источник справочника - Excel
SPR_SOURCE_CSV = '.CSV'   # источник справочника - файлы .csv
CSV_DELIMITER = ';'  # разделитель в CSV файле
DEFAULT_SPR_FILE_NAME = "./SPR/spr_b.xlsx"


log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file=os.path.abspath('./LOGS/scan_spr.log'),
                                   log_level=Lib.ERROR)


class WrongSprExt(Exception):
    """Неверное расширение имени справочника"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SprFilesNotFound(Exception):
    """Файлы справочников не найдены"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Spr(object):
    """
    Класс справочника
    Загружает справочник из:
        1. XLSX - в качестве параметра конструктору передается имя файла.
           Загрузка производится со всех листов файла, формируется список словарей.
           Пустые строки и графы предварительно удаляются. В словарь загружаются первые две графы
           из отсортированного списка
           Поиск производится по всем словарям, при логгировании уровня DEBUG пишется информация
           о не найденных значениях.
           Справочники могут начинаться с любой ячейки
        2. CSV - в качестве параметра указывается маска файлов. Загрузка производится из всех
           найденных файлов, формируется список словарей.
    """
    def __init__(self, spr_file=DEFAULT_SPR_FILE_NAME):
        self.__list_values: list[dict[Any, Any]] = []
        self.__spr_list = None
        base, ext = os.path.splitext(spr_file)
        if ext.upper() not in (SPR_SOURCE_XLS, SPR_SOURCE_CSV):
            raise WrongSprExt(f'{ext} - Неверное расширение имени файла справочника')
        if ext.upper() == SPR_SOURCE_XLS:  #Excel
            try:
                self.__wb = openpyxl.load_workbook(spr_file)  #Загрузка книги Excel
                self.__spr_list = self.__wb.sheetnames  # Формирование списка листов книги
                for ws in self.__spr_list:  # Перебор всех листов книги
                    values = list(self.__wb[ws].values)  # Загрузка значений с листа книги
                    #
                    # Функция возвращае False если все элементы списка row равны "None"
                    def filter_empty_row(row) -> bool:
                        for element in row:
                            if element is not None:
                                return True
                        return False
                    filtered_values = [[e for e in row if e is not None] for row in values if filter_empty_row(row)]
                    # С каждого листа добавление справочника в список как словарь
                    # Из списка значений удалены пустые строки и столбцы
                    # Для словаря делается срез из первых двух столбцов
                    self.__list_values.append(dict([e[:2] for e in filtered_values]))
            except Exception as e:
                log.error(f'Ошибка справочника {spr_file}')
                self.__list_values = None

        elif ext.upper() == SPR_SOURCE_CSV:  # CSV
            try:
                path_file = os.path.split(os.path.abspath(spr_file)) # абсолютный путь списка файлов по маске
                #Формирование списка найденных файлов
                self.__spr_list = list(map(str, sorted(pathlib.Path(path_file[0]).glob(path_file[1]))))
                if len(self.__spr_list) == 0:
                    raise SprFilesNotFound(f'Файлы справочников не найдены: {path_file}')
                for ws in self.__spr_list: #Перебор файлов
                    with open(ws, 'r', newline='') as csvfile: # Для каждого файла:
                        # Загрузка данных из файла
                        s = csv.reader(csvfile, csv.excel, delimiter=CSV_DELIMITER, quoting=csv.QUOTE_NONE)
                        # Добавление словаря в список
                        self.__list_values.append(dict(s))
            except Exception as e:
                log.error(str(e))
                self.__list_values = None

    def find_by_key(self, key) -> str:
        """
        Поиск значения по ключу
        :param key: - ключ поиска (первая колонка в справочнике)
        :return: - найденное значение (вторая колонка в справочнике), иначе - None
        """
        result = ''
        for spr, spr_name in zip(self.__list_values, self.__spr_list):  # Перебор словарей
            if key in spr:
                return str(spr[key])
        log.debug(f"<{key}> не найден в справочнике")
        return result


    @property
    def spr_list(self):
        return self.__spr_list

    @property
    def list_values(self):
        return self.__list_values

    @property
    def values(self):
        return self.__list_values[0]


