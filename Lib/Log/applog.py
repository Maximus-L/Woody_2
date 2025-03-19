# -*- coding: utf-8 -*-
import logging
import os
# 0 Настройка python сообщений
LOG_FILE = "main.log"
INFO = logging.INFO
ERROR = logging.ERROR
DEBUG = logging.DEBUG

"""
1 Выводит сообщения при возникновении незарегистрированных ошибок 
  (например, при возникновении ошибки при освобождении дескрипторов и дескрипторов OCI)
2   Печатает сообщения, когда счетчики ссылок добавляются и освобождаются
4  Выводит сообщения при вызове общедоступной функции ODPI-C. 
8  Печатает сообщения при возникновении ошибки
16 Печатает текст всех подготовленных SQL. Значения привязки не отображаются. 
32 Выводит расположение и размер всех выделений и освобождений памяти, выполненных библиотекой. 
64 Печатает найденные методы и места для библиотеки Oracle Client в дополнение к любым имевшим место ошибкам. 
"""


def AppLogger(name: str,
              output='BOTH',
              log_file=LOG_FILE,
              log_level=ERROR) -> logging.Logger:
    output = 'BOTH' if output not in ['BOTH', 'FILE', 'CONSOLE'] else output
    logger = logging.Logger(name, level=log_level)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(log_level)
    fileHandler = logging.FileHandler(log_file, mode='a', encoding='UTF-8')
    log_format = '{asctime} {name} {filename} #{lineno}-{levelname:8}: {message}'
    # formatter = logging.Formatter('%(asctime)s [%(name)s %(filename)s #%(lineno)d]-%(levelname)s: %(message)s')
    formatter = logging.Formatter(log_format, style="{")
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    if output == 'CONSOLE' or output == 'BOTH':
        logger.addHandler(consoleHandler)
    if output == 'FILE' or output == 'BOTH':
        logger.addHandler(fileHandler)
    if log_level == DEBUG:
        os.environ['DPI_DEBUG_LEVEL'] = str(64 + 32 + 16)
    elif log_level == ERROR:
        os.environ['DPI_DEBUG_LEVEL'] = str('')
    else:
        os.environ['DPI_DEBUG_LEVEL'] = str(16)
    return logger
