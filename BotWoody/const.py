# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

# загрузка файла конфигурации
dotenv_path = './.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# -------------------------------------------------------------
# =============================================================
# TELEGRAM BOT-+=
# -------------------------------------------------------------
BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
BOT_ADMINS = [5172447001]  # , 1280985750]
#                        KuznecovAO
BOT_USERS = [5172447001, 1919089583]
#                            Koryahova  KuznecovAO
BOT_OPERATORS = [5172447001, 803218706, 1919089583]

BOT_USER_ROLES = [['Пользователь', 'user'],
                  ['Оператор', 'operator'],
                  ['Админ', 'admin'],
                  ['Гость', 'guest']]

BOT_KEYS_USERS_OPERATIONS = [['Список', 'list'],
                             ['Добавить', 'add'],
                             ['Задача', 'task']]
BOT_KEYS_USER_OPERATION = [['Изменить', 'update'],
                           ['Удалить', 'del']]

BOT_HELP_ADM_COMMANDS = [
    "/help - справка по командам",
    "/urls - ссылки на страницы с данными",
    "/list - список файлов в хранилище",
    "/get - запрос файла из хранилища",
    "/id - id пользователя",
    "/cron - расписание сканирования",
    "/user - управление пользователями",
    "/cancel - выход из режима"
]

BOT_HELP_OPERATOR_COMMANDS = [
    "/help - справка по командам",
    "/urls - ссылки на страницы с данными",
    "/list - список файлов в хранилище",
    "/get - запрос файла из хранилища",
    "/id - id пользователя",
    "/cancel - выход из режима"
]


BOT_HELP_USER_COMMANDS = [
    "/help - справка по командам",
    "/urls - ссылки на страницы с данными",
    "/list - список файлов в хранилище",
    "/id - id пользователя",
    "/cancel - выход из режима"
]

BOT_HELP_GUEST_COMMANDS = [
    "/help - справка по командам",
    "/id - id пользователя"
]


FILE_REQUEST_TIMEOUT = 300

BOT_KEY_ICONS = ['🗃️', '📁', '🌐', '⏰', '🏷️', '👤']

# -------------------------------------------------------------
# =============================================================
# E-MAIL-+=
# -------------------------------------------------------------
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_APP_NAME = os.environ.get('EMAIL_APP_NAME')
EMAIL_LOGIN = os.environ.get('EMAIL_LOGIN')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_MAX_FILE_SIZE = os.environ.get('EMAIL_MAX_FILE_SIZE')
