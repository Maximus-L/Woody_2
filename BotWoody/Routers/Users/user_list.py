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
                       F.data.in_(['list']))
async def cmd_user_list(callback: CallbackQuery, state: FSMContext):
    keys = []
    for user_id in DbRedis.get_users_by_role():
        user_detail = DbRedis.get_user_detail(str(user_id))
        keys.append([f"[{str(user_id)}] {user_detail['name']} ({user_detail['role']})", str(user_id)])
    await callback.message.delete()
    await callback.message.answer('Пользователи:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=5))
    # установка в состояние выбора действия над пользователем
    await state.set_state(BotWoody.WoodyStates.state_cmd_user_list)


@router.callback_query(BotWoody.WoodyStates.state_cmd_user_list,
                       F.data.in_([str(x) for x in DbRedis.get_users_by_role()]))
async def cmd_user_list_choice_user_operation(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.data)
    keys = BotWoody.BOT_KEYS_USER_OPERATION
    await callback.message.delete()
    await callback.message.answer(f'Пользователь [{callback.data}]:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=5))
    # установка в состояние добавления пользователя и ввода ID
    await state.set_state(BotWoody.WoodyStates.state_cmd_user_list_choice_user)


@router.callback_query(BotWoody.WoodyStates.state_cmd_user_list_choice_user,
                       F.data.in_(['del']))
async def cmd_user_list_choice_user_del(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    await callback.message.delete()
    if DbRedis.db_user_del(user_id):
        await callback.message.answer(text=f'Удален пользователь [{user_id}]')
        await BotWoody.bot.send_message(int(user_id), 'Ваш ID удален из БД пользователей.')
    await state.clear()
