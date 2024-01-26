# -*- coding: utf-8 -*-
import asyncio

import aiocron
from aiogram import Bot, Dispatcher

# import DbUsers
import Lib
import BotWoody.Routers
import BotWoody


log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/bot.log',
                                   log_level=Lib.INFO)

# Инициализация БД с пользователями
# BotWoody.db_users = DbUsers.DbProvider(connstr=DbUsers.sqlite_str)

# Инициализация источников данных
BotWoody.data_storages = BotWoody.data_stores_init()

# Инициализация бота
BotWoody.bot = Bot(token=BotWoody.BOT_API_TOKEN, parse_mode='HTML')
dp = Dispatcher()


# @aiocron.crontab('0 4 * * *')
# async def msg_tst():
#     log.info('Start checking')
#     await BotWoody.bot.send_message(BotWoody.const.BOT_ADMINS[0], '---')


@aiocron.crontab('*/10 * * * *')
async def check_stores():
    # print('checking...')
    for store in BotWoody.data_storages:
        await BotWoody.data_store_check(store,
                                        users_email=['larinma@cbr.ru'])


def tst_send_mail():
    import smtplib as smtp

    login = 'vomit2180@gmail.com'
    password = 'bhvy utfg keqp oiag'

    server = smtp.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(login, password)

    subject = 'MSP testing'
    text = 'msp-2023-11-01'

    server.sendmail(login, to_addrs='larinma@cbr.ru', msg=f'Subject:{subject}\n{text}')


async def main():
    # Подключение роутеров
    dp.include_router(BotWoody.Routers.router_help)
    dp.include_router(BotWoody.Routers.router_urls)
    dp.include_router(BotWoody.Routers.router_list)
    dp.include_router(BotWoody.Routers.router_get)
    dp.include_router(BotWoody.Routers.router_adm_cron)
    # dp.include_router(BotWoody.Routers.router_test)
    dp.include_router(BotWoody.Routers.router_others)
    log.info('Bot started!')
    # await BotWoody.db_users.create_engine()
    # print(await BotWoody.db_users.get_roles())
    task = asyncio.create_task(BotWoody.msg_adm_started(BotWoody.bot))
    await BotWoody.bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(BotWoody.bot)
    await task


if __name__ == '__main__':
    # tst_send_mail()
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()

