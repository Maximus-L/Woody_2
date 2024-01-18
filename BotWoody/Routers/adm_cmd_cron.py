# -*- coding: utf-8 -*-
# Роутер по команде /cron
# Выводит сообщение о расписании сканирования сайтов
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

import BotWoody.const as const
import Scaner

router = Router()


@router.message(Command(commands=['cron']),
                F.from_user.id.in_(const.BOT_ADMINS))
async def cmd_help_answer_adm(message: Message):
    await message.answer(text="Расписания:",
                         reply_markup=ReplyKeyboardRemove())
    for name in Scaner.DATA_SOURCE.keys():
        await message.answer(text=f"{name}: [{Scaner.DATA_SOURCE[name]['cron']}]")
