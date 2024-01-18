# -*- coding: utf-8 -*-
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardRemove,
                           CallbackQuery, FSInputFile)

from aiogram.fsm.context import FSMContext


import BotWoody
import Scaner

import BotWoody.const as const

router = Router()
a = BotWoody.db_users.get_users_of_role(role='ADMIN')

# Обработка команды /get
@router.message(Command(commands=['tst']),
                F.from_user.id.in_(a))
async def cmd_get_answer(message: Message, state: FSMContext):
    keys = []
    for name in Scaner.DATA_SOURCE.keys():
        keys.append([Scaner.DATA_SOURCE[name]['description'], name])
    await message.answer(text="Выберите источник:",
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=1))
    # установка состояния в ожидание выбора источника
    await state.set_state(BotWoody.WoodyStates.state_cmd_get)

