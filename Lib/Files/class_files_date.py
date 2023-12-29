# -*- coding: utf-8 -*-
import os
import fnmatch
import re
import datetime as dt
from pathlib import Path

import Lib


log: Lib.AppLogger = Lib.AppLogger('Class FileStore',
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.ERROR)


class InvalidFilePath(Exception):
    def __init__(self, message_path):
        self.message = f'Неверно указан путь: {message_path}'
        super().__init__(self.message)


class FilesStore(object):
    def __init__(self, files_path,
                 date_re='data-\d{8}',
                 date_format='data-%d%m%Y'):
        """
        Инициализация экземпляра класса хранилища файлов
        :param files_path: Путь и маска файлов хранилища
        :param date_re: Регулярное выражение для поиска даты в имени файла
        :param date_format: Формат даты в имени файла
        """
        self.__files_path, self.__file_mask = os.path.split(files_path)
        base, self.__ext = os.path.splitext(files_path)
        self.__date_mask = date_re
        self.__date_format = date_format
        self.__last_file = ""
        self.file_list = {}  # Список файлов в хранилище - словарь, ключом является дата
        # Генерирование исключения в случае отсутствия папки
        if not os.path.exists(self.__files_path):
            log.error(f'Неверно указан путь: {self.__files_path}')
            raise InvalidFilePath(self.__files_path)
        self.__full_path = os.path.abspath(self.__files_path)
        # Перебор файлов в папке по маске
        for rootkit, subdir, filenames in os.walk(self.__full_path):
            for filename in fnmatch.filter(filenames, self.__file_mask):
                # Поиск регулярки даты в имени файла
                s_date = re.search(self.__date_mask, filename)
                if s_date is not None:
                    # Если найдено - перевод в дату
                    d1 = dt.datetime.strptime(s_date.group(0), date_format)
                    date = dt.date(d1.year, d1.month, 1)
                    # Добавление файла в словарь
                    self.file_list[date] = filename
        log.debug(list(str(a) for a in self.file_list.keys()))

    def refresh(self):
        """
        Обновление информации о файлах в хранилище
        :return:
        """
        refreshed = False
        current_dates = self.file_list.keys()
        self.file_list.clear()
        for rootkit, subdir, filenames in os.walk(self.__full_path):
            for filename in fnmatch.filter(filenames, self.__file_mask):
                s_date = re.search(self.__date_mask, filename)
                if s_date is not None:
                    d1 = dt.datetime.strptime(s_date.group(0), self.__date_format)
                    date = dt.date(d1.year, d1.month, 1)
                    self.file_list[date] = filename
                    if date not in current_dates:
                        refreshed = True
                        log.debug(f'Новая дата:{date}')
        return refreshed

    @property  # Путь по которому хранятся файлы
    def store_path(self):
        return self.__files_path

    @property  # Дата последнего файла
    def last_date(self):
        if self.count > 0:
            return max(list(self.file_list.keys()))
        else:
            return None

    @property  # Количество файлов в хранилище
    def count(self):
        return len(self.file_list)

    @property  # Тип файлов в хранилище
    def files_type(self):
        return self.__ext[1:].upper()

    @property
    def last_date_file_name(self):
        if self.count > 0:
            self.__last_file = Path(self.__files_path) / self.file_list[self.last_date]
            return self.__last_file
        else:
            return None
