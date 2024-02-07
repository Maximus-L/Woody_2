# -*- coding: utf-8 -*-
# Роутер по команде /help
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
import Lib

router = Router()

log: Lib.AppLogger = Lib.AppLogger(__name__, output='BOTH',
                                   log_file='./LOGS/bot.log',
                                   log_level=Lib.DEBUG)

delete_words = ["блять", "сука", "хуй", "ебал", "пизда", "пизду",
                "хуёвый", "хуета", "пизди", "бляд", "курва", "мудак"]


@router.message()
async def cmd_help_answer_other(message: Message):
    if message.text:
        if any(word in message.text.lower() for word in delete_words):
            log.debug(f'[{message.from_user.id}][{message.from_user.username}]: "{message.text}"')
            await message.answer(text="Будешь материться - забаню к херам!",
                                 reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Список команд: /help",
                         reply_markup=ReplyKeyboardRemove())
