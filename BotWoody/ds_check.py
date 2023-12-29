# -*- coding: utf-8 -*-
import os

from aiogram.types import FSInputFile
import smtplib as smtp

import BotWoody
import Lib

import BotWoody.const as const
import Scaner.const as scan_const

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/bot.log',
                                   log_level=Lib.ERROR)


async def data_store_check(store: Lib.DLStore,
                           users_msg=const.BOT_USERS,
                           users_file=const.BOT_OPERATORS,
                           users_email=None):
    """
    Проверка хранилища на новые файлы.
    :param users_email: список адресов для рассылки данных
    :param users_msg: list список пользователей кому отправлять сообщение
                       когда появляется новый файл
    :param users_file: list список пользователей кому отправлять файл
                       когда появляется новый файл
    :param store: экземпляр хранилища
    :return: None
    """
    new = store.refresh()
    if new is not None and new:
        # Тут надо определить список пользователей кому и что отправлять
        # возможно msg_type будет не нужен
        if users_msg:
            for user in users_msg:
                message = f'!! New: {scan_const.DATA_SOURCE[store.name]["description"]} - {store.store_last_date}'
                try:
                    await BotWoody.bot.send_message(user, message)
                except Exception as e:
                    log.error(f'ошибка пользователя {user}, {e}')
        if users_file:
            for user in users_file:
                filename = store.store_list[store.store_last_date]
                filepath = os.path.join(store.store_p, filename)
                f = FSInputFile(str(filepath), filename)
                try:
                    await BotWoody.bot.send_document(user, f,
                                                     request_timeout=const.FILE_REQUEST_TIMEOUT)
                except Exception as e:
                    log.error(f'ошибка пользователя {user}, {e}')
        if users_email:
            for user in users_email:
                try:
                    with smtp.SMTP(host=const.EMAIL_HOST, port=const.EMAIL_PORT) as server:
                        server.starttls()
                        server.login(const.EMAIL_LOGIN, const.EMAIL_PASSWORD)
                        subject = scan_const.DATA_SOURCE[store.name]["description"]
                        text = 'Новые данные!!!'
                        server.sendmail(const.EMAIL_LOGIN,
                                        to_addrs=user,
                                        msg=f'Subject:{subject}\n{text}')
                except Exception as e:
                    log.error(f'e-mail: {user} {e}')
