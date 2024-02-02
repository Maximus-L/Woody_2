# -*- coding: utf-8 -*-

import datetime as dt
import os.path

# owner's lib
import Lib
import Parser.last_date
import Parser.download_arc
import Lib.Files.archive

STORE_DATE_RE = '\d{4}-\d{2}-\d{2}'
STORE_DATE_FORMAT = '%Y-%m-%d'
STORE_PATH_DEFAULT = './OUT'

STORE_PATH_TMP = './TEMP'

log: Lib.AppLogger = Lib.AppLogger('Class DLStore',
                                   output='BOTH',
                                   log_file='./LOGS/scaner.log',
                                   log_level=Lib.ERROR)


class DLStore(object):
    """
    Класс хранилища данных
    """

    def __init__(self,
                 name='Store',
                 url='https://cbr.ru',
                 store_path=STORE_PATH_DEFAULT,
                 store_prefix='out',
                 store_ext='csv',
                 archive_path=None,
                 archive_date_re=None,
                 archive_date_format=None,
                 temp_path=None,
                 spr_file='./SPR/region.xlsx'):
        """
        :param name: - Условное имя хранилища. Используется при вызовах методов:
                       get_last_date_url, download_to_arc, download_to_csv
                       Из указанных методов вызываются функции обработки. В зависимости от
                       имени хранилища вызываются соответствующие обработчики
                       (модули Parser.download_arc, Parser.last_date, Parser.parse2csv)
        :param url: - адрес страницы с данными
        :param store_path: - путь к обработанным файлам (CSV)
        :param store_prefix: - префикс наименования CSV-файлов
        :param store_ext: - расширение файлов в хранилище (по умолчанию CSV)
        :param archive_path: - указывается в случае скачивания с сайтов zip файлов
        :param archive_date_re: - регулярное выражение для поиска даты в имени zip файла
        :param archive_date_format: - формат для преобразования даты из имени файла
        :param temp_path: - путь куда будут распакованы файлы из архива для дальнейшей обработке
        :param spr_file: - имя файла справочника (в основном регионов). По имени файла создается
                           экземпляр класса Lib.Spr (модуль Lib.Spr.class_spr). Используется в
                           обработке данных. Передается в качестве параметра в функции.
        """
        self.name = name.upper()
        self.url = url
        self.__url_last_date = None
        self.__url_last_url = None
        self.__arc_last_loaded_file = None
        self.__temp_path = temp_path
        self.__spr = Lib.Spr(spr_file) if spr_file is not None else None
        self.store_p = os.path.abspath(store_path)
        try:
            # создание файлового хранилища для csv файлов
            self.__store = Lib.FilesStore(os.path.join(self.store_p, store_prefix + '*.' + store_ext),
                                          store_prefix + STORE_DATE_RE,
                                          store_prefix + STORE_DATE_FORMAT)
        except Exception as e:
            log.error(e)
            raise e
        # если определено хранилище для zip - создание экземпляра класса Lib.Files.FilesStore
        if archive_path is not None and \
                archive_date_re is not None and \
                archive_date_format is not None:
            try:
                self.__archive_store: Lib.FilesStore = Lib.FilesStore(archive_path,
                                                                      archive_date_re,
                                                                      archive_date_format)
                self.__arc_last_loaded_file = self.__archive_store.last_date_file_name
            except Exception as e:
                log.error(e)
                raise e
        else:
            self.__archive_store = None

    def get_last_date_url(self) -> dt.date | None:
        """
        :return: возвращает дату самых "свежих" данных на странице self.url
        """
        self.__url_last_date, self.__url_last_url = Parser.url_data_last_date(self.name, self.url)
        return self.__url_last_date

    def download_to_arc(self):
        """
        Метод загружает zip файл в хранилище
        :return: имя загруженного файла. при сбое загрузки None
        """
        try:
            self.__arc_last_loaded_file = Parser.download_arc(self.name,
                                                              self.__url_last_url,
                                                              self.__archive_store.store_path)
            self.__archive_store.refresh()
            return self.__arc_last_loaded_file
        except Exception as e:
            log.error(f'Не загружен zip: {self.url}. {e}')
            return None

    def download_to_csv(self, date=None):
        csv_name = Parser.parse2csv(self.name,
                                    url=self.url if self.__temp_path is None else self.__temp_path,
                                    spr_regions=self.__spr,
                                    date=self.__url_last_date if date is None else date,
                                    csv_path=self.__store.store_path,
                                    store=self)
        self.__store.refresh()
        res_zip_path = os.path.join(self.__store.store_path, 'zip')
        if os.path.isdir(res_zip_path):
            fname = os.path.split(csv_name)[1]
            zip_name = os.path.join(res_zip_path, os.path.splitext(fname)[0]+'.zip')
            Lib.Files.zip_file(csv_name, zip_name)
        else:
            log.info(f'Not archived: {csv_name}')
        return csv_name

    def extract_arc(self, date: dt.date = None):
        if date is not None and date in self.archive_store_list.keys():
            zip_file_name = self.archive_store_list[date]
        else:
            zip_file_name = self.__arc_last_loaded_file
        if zip_file_name is not None and self.__temp_path is not None:
            Lib.Files.unzip_file(os.path.join(self.__archive_store.store_path, zip_file_name),
                                 self.__temp_path)

    def refresh(self):
        if self.__archive_store is None:
            return self.__store.refresh()
        else:
            return [self.__store.refresh(), self.__archive_store.refresh()]

    @property
    def store_list(self):
        """
        :return: список CSV файлов в хранилище (словарь, ключ - дата)
        """
        return self.__store.file_list

    @property
    def store_last_date(self):
        """
        :return: дата "свежих" данных в CSV файле в хранилище
        """
        return self.__store.last_date

    @property
    def archive_store_list(self):
        """
        :return: список ZIP файлов в хранилище (словарь, ключ - дата)
        """
        return self.__archive_store.file_list

    @property
    def archive_store_last_date(self):
        """
        :return: дата "свежего" ZIP файла в хранилище
        """
        return self.__archive_store.last_date

    @property
    def store_path(self):
        """
        :return: полный путь к файлам хранилища
        """
        return self.store_p
