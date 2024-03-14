# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardRemove,
                           CallbackQuery, FSInputFile)

from aiogram.fsm.context import FSMContext

import BotWoody
import BotWoody.Routers

import DbRedis

import BotWoody.const as const
from BotWoody import BOT_LANG

router = Router()


@router.callback_query(BotWoody.WoodyStates.state_cmd_user,
                       F.data.in_(['add']))
async def cmd_user_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Введите ID нового пользователя:',
                                  reply_markup=ReplyKeyboardRemove())
    # установка в состояние добавления пользователя и ввода ID
    await state.set_state(BotWoody.WoodyStates.state_cmd_user_add)


@router.message(BotWoody.WoodyStates.state_cmd_user_add)
async def cmd_user_add_id(message: Message, state: FSMContext):
    user_id = message.text
    if user_id.isdigit() and int(user_id) not in DbRedis.get_users_by_role():
        await state.update_data(user_id=user_id)
        await message.answer(text='Введите ИМЯ нового пользователя:',
                             reply_markup=ReplyKeyboardRemove())
        # установка в состояние добавления пользователя и ввода ID
        await state.set_state(BotWoody.WoodyStates.state_cmd_user_add_id)
    else:
        await message.answer(text='ID пользователя не цифровое или пльзователь существует!',
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(text=BOT_LANG['wrong choice'])


@router.message(BotWoody.WoodyStates.state_cmd_user_add_id)
async def cmd_user_add_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    keys = const.BOT_USER_ROLES
    await message.answer(text=BOT_LANG['/user role choice'],
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=5))
    # установка в состояние ожидания ввода роли
    await state.set_state(BotWoody.WoodyStates.state_cmd_user_add_name)


@router.callback_query(BotWoody.WoodyStates.state_cmd_user_add_name,
                       F.data.in_([r[1] for r in const.BOT_USER_ROLES]))
async def cmd_user_add_role(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user = await state.get_data()
    role = callback.data
    if DbRedis.db_user_add(user_id=user['user_id'], role=role, username=user['user_name']):
        await callback.message.answer(f'Добавлен в БД пользователь: {user["user_id"]} {user["user_name"]} {role}',
                                      reply_markup=ReplyKeyboardRemove())
        await BotWoody.bot.send_message(int(user['user_id']),
                                        text=f'Ваш ID добавлен в  БД пользователей с ролью ({role})')
    # установка в состояние добавления пользователя и ввода ID
    await state.clear()
