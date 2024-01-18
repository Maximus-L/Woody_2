# -*- coding: utf-8 -*-
import mimetypes
import os

from aiogram.types import FSInputFile
import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import EmailMessage

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
            filename = store.store_list[store.store_last_date]
            filepath = os.path.join(store.store_p, filename)
            for user in users_file:
                try:
                    f = FSInputFile(str(filepath), filename)
                    await BotWoody.bot.send_document(user, f,
                                                     request_timeout=const.FILE_REQUEST_TIMEOUT)
                except Exception as e:
                    log.error(f'ошибка пользователя {user}, {e}')
        if users_email:
            filename = store.store_list[store.store_last_date]
            filepath = os.path.join(store.store_p, filename)
            send_email_attach(msg_to=users_email,
                              msg_subj=scan_const.DATA_SOURCE[store.name]["description"],
                              attachment_file=filepath,
                              filename=filename)
            # for user in users_email:
            #     try:
            #         with smtp.SMTP(host=const.EMAIL_HOST, port=const.EMAIL_PORT) as server:
            #             server.starttls()
            #             server.login(const.EMAIL_LOGIN, const.EMAIL_PASSWORD)
            #             subject = scan_const.DATA_SOURCE[store.name]["description"]
            #             text = 'Новые данные!!!'
            #             server.sendmail(const.EMAIL_LOGIN,
            #                             to_addrs=user,
            #                             msg=f'Subject:{subject}\n{text}')
            #     except Exception as e:
            #         log.error(f'e-mail: {user} {e}')


def send_email_attach(msg_to, msg_subj, attachment_file, filename):
    file_size = os.path.getsize(attachment_file)
    # Если размер файла > 1Mb
    if file_size > const.EMAIL_MAX_FILE_SIZE:
        log.info(f'Не отправлен: {filename}, размер={file_size}')
        return None
    msg = EmailMessage()
    msg['Subject'] = f'Отправка: {msg_subj}'
    msg['To'] = ', '.join(msg_to)
    msg['From'] = 'Woody Woodpecker'  # const.EMAIL_LOGIN

    ctype, encoding = mimetypes.guess_type(attachment_file)
    if ctype is None or encoding is not None:
        # Невозможно сделать предположение, или файл закодирован (сжат), поэтому
        # используйте общий тип пакета битов.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(attachment_file, 'rb') as fp:
        msg.add_attachment(fp.read(),
                           maintype=maintype,
                           subtype=subtype,
                           filename=filename)
    try:
        with smtp.SMTP(host=const.EMAIL_HOST, port=const.EMAIL_PORT) as server:
            server.starttls()
            server.login(const.EMAIL_LOGIN, const.EMAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        log.error(f'e-mail: {msg["To"]} {e}')

