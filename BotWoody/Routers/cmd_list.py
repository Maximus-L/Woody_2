# -*- coding: utf-8 -*-

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

import BotWoody
import Scaner
import BotWoody.const as const

router = Router()


@router.message(Command(commands=['list']),
                F.from_user.id.in_(const.BOT_ADMINS))
@router.message(Command(commands=['list']),
                F.from_user.id.in_(const.BOT_USERS))
@router.message(Command(commands=['list']),
                F.from_user.id.in_(const.BOT_OPERATORS))
async def cmd_list_answer(message: Message, state: FSMContext):
    keys = []
    for name in Scaner.DATA_SOURCE.keys():
        keys.append([Scaner.DATA_SOURCE[name]['description'], name])
    await message.answer(text="Выберите источник:",
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=1))
    # установка состояния в ожидание выбора источника
    await state.set_state(BotWoody.WoodyStates.state_cmd_list)


@router.callback_query(BotWoody.WoodyStates.state_cmd_list,
                       F.data.in_(Scaner.DATA_SOURCE.keys()))
async def cmd_list_choice_src(callback: CallbackQuery, state: FSMContext):
    # Извлечение имени источника
    name = callback.data
    await callback.message.delete()
    await callback.message.answer(name)
    await callback.answer(text="Список файлов:",
                          reply_markup=ReplyKeyboardRemove())
    # Формирование списка файлов
    for ds in BotWoody.data_storages:
        if ds.name == name:
            for date in ds.store_list.keys():
                await callback.message.answer(text='🏷️'+ds.store_list[date])
    await state.clear()


# Отмена команды
@router.message(BotWoody.WoodyStates.state_cmd_list,
                Command(commands=['cancel', 'clr']))
async def cmd_list_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Отменено.",
                         reply_markup=ReplyKeyboardRemove())


# Реакция на неправильный выбор источника данных
@router.message(BotWoody.WoodyStates.state_cmd_list)
async def cmd_list_wrong_src(message: Message):
    keys = []
    for name in Scaner.DATA_SOURCE.keys():
        keys.append([Scaner.DATA_SOURCE[name]['description'], name])
    await message.answer(text="Такого источника нет. Выберите из списка:",
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys))
