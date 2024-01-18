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


# Обработка команды /get
@router.message(Command(commands=['get']),
                F.from_user.id.in_(const.BOT_OPERATORS))
@router.message(Command(commands=['get']),
                F.from_user.id.in_(const.BOT_ADMINS))
async def cmd_get_answer(message: Message, state: FSMContext):
    keys = []
    for name in Scaner.DATA_SOURCE.keys():
        keys.append([Scaner.DATA_SOURCE[name]['description'], name])
    await message.answer(text="Выберите источник:",
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=1))
    # установка состояния в ожидание выбора источника
    await state.set_state(BotWoody.WoodyStates.state_cmd_get)


# Выбор источника данных
@router.callback_query(BotWoody.WoodyStates.state_cmd_get,
                       F.data.in_(Scaner.DATA_SOURCE.keys()))
async def cmd_get_choice_src(callback: CallbackQuery, state: FSMContext):
    # Извлечение имени источника
    name = callback.data
    await callback.message.delete()
    await state.update_data(chosen_source=name)
    await callback.message.answer(name)
    files = []
    for ds in BotWoody.data_storages:
        if ds.name == name:
            await state.update_data(store_path=ds.store_p)
            for date in ds.store_list.keys():
                files.append([ds.store_list[date], ds.store_list[date]])
    if len(files) > 0:
        await callback.message.answer(
            text="Выберите файл для скачивания:",
            reply_markup=BotWoody.inline_keyboard_cb_data(files, size=1))
    # установка в состояние выбора файла для скачивания
    await state.set_state(BotWoody.WoodyStates.state_cmd_get_filechoice)


# Выбор файла данных
@router.callback_query(BotWoody.WoodyStates.state_cmd_get_filechoice)
async def cmd_get_choice_file(callback: CallbackQuery, state: FSMContext):
    # Извлечение имени файла
    file_name = callback.data
    await callback.message.delete()
    await callback.message.answer(f'Выгрузка: {file_name} ...')
    user_data = await state.get_data()
    filepath = os.path.join(user_data['store_path'], file_name)
    f = FSInputFile(filepath, file_name)
    user = callback.from_user.id
    await BotWoody.bot.send_document(user, f,
                                     request_timeout=const.FILE_REQUEST_TIMEOUT)
    await callback.message.answer('Готово!')
    await state.clear()


# Отмена команды
@router.message(BotWoody.WoodyStates.state_cmd_get_filechoice,
                Command(commands=['cancel'])
                )
@router.message(BotWoody.WoodyStates.state_cmd_get,
                Command(commands=['cancel'])
                )
async def cmd_get_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено: /get', reply_markup=ReplyKeyboardRemove())


# Реакция на ошибку выбора источника или файла
@router.message(BotWoody.WoodyStates.state_cmd_get)
@router.message(BotWoody.WoodyStates.state_cmd_get_filechoice)
async def cmd_get_wrong(message: Message):
    await message.answer('Попробуйте еще или /cancel')
