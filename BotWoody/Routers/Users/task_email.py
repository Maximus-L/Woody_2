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
                       F.data.in_(['task']))
async def cmd_task_list(callback: CallbackQuery, state: FSMContext):
    keys = []
    for task_name in DbRedis.get_task_list():
        keys.append([f"[{task_name}]", task_name])
    await callback.message.delete()
    await callback.message.answer('Задачи:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=5))
    # установка в состояние выбора действия над пользователем
    await state.set_state(BotWoody.WoodyStatesTask.state_wait_choice)


@router.callback_query(BotWoody.WoodyStatesTask.state_wait_choice)
async def cmd_task_list(callback: CallbackQuery, state: FSMContext):
    keys = []
    await state.update_data(task=callback.data)
    for user_id in DbRedis.db_task_get_users_email(callback.data):
        user_name = DbRedis.get_user_detail(user_id)[DbRedis.R_USERS_NAME_KEY]
        keys.append([f"[{user_id}] - {user_name}", user_id])
    await callback.message.delete()
    await callback.message.answer(f'Пользователи для задачи [{callback.data}]:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=5))
    # установка в состояние выбора действия над пользователем
    await state.set_state(BotWoody.WoodyStatesTask.state_wait_user)
