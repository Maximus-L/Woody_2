# -*- coding: utf-8 -*-
import asyncio

import aiocron
from aiogram import Bot, Dispatcher
import redis

import DbRedis
# import DbUsers
import Lib
import BotWoody
import BotWoody.Routers


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
    operators = DbRedis.get_users_by_role(['operator'])
    users = DbRedis.get_users_by_role(['user'])
    for store in BotWoody.data_storages:
        emails = DbRedis.db_task_get_emails(task_name=store.name)
        await BotWoody.data_store_check(store,
                                        users_msg=users,
                                        users_file=operators,
                                        users_email=emails)


async def main():
    # Подключение роутеров
    # BotWoody.r = redis.Redis(host="localhost", port=6379)
    dp.include_router(BotWoody.Routers.router_help)
    dp.include_router(BotWoody.Routers.router_urls)
    dp.include_router(BotWoody.Routers.router_list)
    dp.include_router(BotWoody.Routers.router_get)
    dp.include_router(BotWoody.Routers.router_user)
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
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()

