# -*- coding: utf-8 -*-

import Lib
import BotWoody.const as const

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/bot.log',
                                   log_level=Lib.ERROR)


async def msg_adm_started(bot, users=const.BOT_ADMINS):
    if users:
        for user in users:
            try:
                await bot.send_message(user, 'Bot started')
            except Exception as e:
                log.error(f'ошибка пользователя {user}, {e}')
    else:
        log.error('Not users for message')

