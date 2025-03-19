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
    # по команде /task выводит список задач
    keys = []
    for task_name in DbRedis.get_task_list():
        keys.append([f"[{task_name}]", task_name])
    await callback.message.delete()
    await callback.message.answer('Задачи:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=5))
    # установка в состояние выбора действия над пользователем
    await state.set_state(BotWoody.WoodyStatesTask.state_wait_choice)


@router.callback_query(BotWoody.WoodyStatesTask.state_wait_choice)
async def cmd_task_list_users(callback: CallbackQuery, state: FSMContext):
    # Вывод списка пользователей для задачи и ожидание выбора пользователя
    # для удаления либо ожидание /add
    keys = []
    await state.update_data(task=callback.data)
    for user_id in DbRedis.db_task_get_users_email(callback.data):
        user_name = DbRedis.get_user_detail(user_id)[DbRedis.R_USERS_NAME_KEY]
        keys.append([f"[{user_id}] - {user_name}", str(user_id)])
    await callback.message.delete()
    await callback.message.answer(f'Пользователи для задачи [{callback.data}] /add - добавить:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=5))
    # установка в состояние выбора действия над пользователем
    await state.set_state(BotWoody.WoodyStatesTask.state_wait_user)


@router.message(BotWoody.WoodyStatesTask.state_wait_user, Command(commands=['add']))
async def cmd_task_list_users_for_add(message: Message, state: FSMContext):
    keys = []
    for user_id in DbRedis.get_users_by_role():
        user_detail = DbRedis.get_user_detail(str(user_id))
        keys.append([f"[{str(user_id)}] {user_detail[DbRedis.R_USERS_NAME_KEY]} ({user_detail[DbRedis.R_USERS_ROLE_KEY]})",
                     str(user_id)])
    await message.answer('Выберите пользователя для добавления:',
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=5))
    await state.set_state(BotWoody.WoodyStatesTask.state_wait_user_for_add)



@router.callback_query(BotWoody.WoodyStatesTask.state_wait_user_for_add)
async def cmd_task_user_add(callback: CallbackQuery, state: FSMContext):
    # добавление пользователя
    data = await state.get_data()
    res = DbRedis.db_task_add_user_email(task_name=data['task'], user_id=callback.data)
    await callback.message.delete()
    await callback.message.answer(f"Пользователь добавлен [{res}]")
    await state.clear()


@router.callback_query(BotWoody.WoodyStatesTask.state_wait_user)
async def cmd_task_user_del_question(callback: CallbackQuery, state: FSMContext):
    # запрос на подтв. удаление пользователя
    user_id = callback.data
    user_detail = DbRedis.get_user_detail(user_id)
    await state.update_data(user_id_del=user_id)
    await callback.message.delete()
    await callback.message.answer(f'Удалить [{user_detail[DbRedis.R_USERS_NAME_KEY]}] [{user_id}]?',
                                  reply_markup=BotWoody.keyboard_yes_no())
    await state.set_state(BotWoody.WoodyStatesTask.state_wait_user_del_yes_no)


@router.callback_query(BotWoody.WoodyStatesTask.state_wait_user_del_yes_no)
async def cmd_task_user_delete(callback: CallbackQuery, state: FSMContext):
    # удаление пользователя
    await callback.message.delete()
    if callback.data == 'YES':
        data = await state.get_data()
        res = DbRedis.db_task_del_user_email(task_name=data['task'], user_id=data['user_id_del'])
        await callback.message.answer(f"Пользователь удален [{res}]")
    await state.clear()
