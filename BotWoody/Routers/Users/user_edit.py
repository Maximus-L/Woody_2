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


@router.callback_query(BotWoody.WoodyStates.state_cmd_user_list_choice_user,
                       F.data.in_(['update']))
async def cmd_user_list_choice_user_update(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    await callback.message.delete()
    user_detail = DbRedis.get_user_detail(user_id)
    print(user_detail)
    if DbRedis.R_USERS_EMAIL_KEY not in user_detail.keys():
        user_detail[DbRedis.R_USERS_EMAIL_KEY] = "-"
    if DbRedis.R_USERS_ENABLED_KEY not in user_detail.keys():
        user_detail[DbRedis.R_USERS_ENABLED_KEY] = 1
    keys = [[f"Имя: [{user_detail[DbRedis.R_USERS_NAME_KEY]}]", DbRedis.R_USERS_NAME_KEY],
            [f"Роль: [{user_detail[DbRedis.R_USERS_ROLE_KEY]}]", DbRedis.R_USERS_ROLE_KEY],
            [f"E-mail: [{user_detail[DbRedis.R_USERS_EMAIL_KEY]}]", DbRedis.R_USERS_EMAIL_KEY],
            [f"Вход разрешен: [{user_detail[DbRedis.R_USERS_ENABLED_KEY]}]", DbRedis.R_USERS_ENABLED_KEY]]
    await state.update_data(name=user_detail[DbRedis.R_USERS_NAME_KEY])
    await state.update_data(role=user_detail[DbRedis.R_USERS_ROLE_KEY])
    await state.update_data(e_mail=user_detail[DbRedis.R_USERS_EMAIL_KEY])
    await state.update_data(enable=user_detail[DbRedis.R_USERS_ENABLED_KEY])
    await callback.message.answer('Параметр для редактирования:',
                                  reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=1))
    await state.set_state(BotWoody.WoodyStatesUserEdit.state_wait_edited_param)


@router.callback_query(BotWoody.WoodyStatesUserEdit.state_wait_edited_param,
                       F.data.in_([DbRedis.R_USERS_NAME_KEY,
                                   DbRedis.R_USERS_ROLE_KEY,
                                   DbRedis.R_USERS_EMAIL_KEY,
                                   DbRedis.R_USERS_ENABLED_KEY]))
async def cmd_user_edit_value_for_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(edit_param=callback.data)
    if callback.data == DbRedis.R_USERS_ROLE_KEY:
        keys = const.BOT_USER_ROLES
        await callback.message.answer(text=BOT_LANG['/user role choice'],
                                      reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=5))
        await state.set_state(BotWoody.WoodyStatesUserEdit.state_wait_role)
    else:
        await callback.message.answer(f'Введите значение для [{callback.data}]:')
        await state.set_state(BotWoody.WoodyStatesUserEdit.state_wait_value)


@router.message(BotWoody.WoodyStatesUserEdit.state_wait_value)
async def cmd_user_edit_value_for_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    param = data['edit_param']
    data[param] = message.text
    DbRedis.db_user_update(user_id, mapping={param: data[param]})
    await message.answer(f'Внесено в БД')
    keys = [[f"Имя: [{data[DbRedis.R_USERS_NAME_KEY]}]", DbRedis.R_USERS_NAME_KEY],
            [f"Роль: [{data[DbRedis.R_USERS_ROLE_KEY]}]", DbRedis.R_USERS_ROLE_KEY],
            [f"E-mail: [{data[DbRedis.R_USERS_EMAIL_KEY]}]", DbRedis.R_USERS_EMAIL_KEY],
            [f"Вход разрешен: [{data[DbRedis.R_USERS_ENABLED_KEY]}]", DbRedis.R_USERS_ENABLED_KEY]]
    await message.answer('Параметр для редактирования:',
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=1, pict=1))
    await state.set_state(BotWoody.WoodyStatesUserEdit.state_wait_edited_param)


@router.callback_query(BotWoody.WoodyStatesUserEdit.state_wait_role,
                       F.data.in_([r[1] for r in const.BOT_USER_ROLES]))
async def cmd_user_edit_role(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    user_id = data['user_id']
    data['role'] = callback.data
    DbRedis.db_user_update(user_id, mapping={'role': data['role']})
    await callback.message.answer(f'Внесено в БД')
