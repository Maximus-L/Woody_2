# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import (Message, ReplyKeyboardRemove)

from aiogram.fsm.context import FSMContext


import BotWoody


import BotWoody.const as const
import BotWoody.Filt as Filt
from BotWoody import BOT_LANG
from .Users import (router_user_add, router_user_list,
                    router_user_edit, router_task_email)

router = Router()
router.include_router(router_user_add)
router.include_router(router_user_list)
router.include_router(router_user_edit)
router.include_router(router_task_email)


# @router.message(Command(commands=['user']))
@router.message(Command(commands=['user']),
                Filt.UsersByRole(['admin']))
async def cmd_get_answer(message: Message, state: FSMContext):
    keys = const.BOT_KEYS_USERS_OPERATIONS
    await message.answer(text=BOT_LANG['/user'],
                         reply_markup=BotWoody.inline_keyboard_cb_data(keys, size=2, pict=5))
    # установка состояния в ожидание выбора действия над пользователем
    await state.set_state(BotWoody.WoodyStates.state_cmd_user)


@router.message(StateFilter(BotWoody.WoodyStates.state_cmd_user), Command(commands=['cancel']))
@router.message(StateFilter(BotWoody.WoodyStates.state_cmd_user_add), Command(commands=['cancel']))
@router.message(StateFilter(BotWoody.WoodyStates.state_cmd_user_list), Command(commands=['cancel']))
@router.message(BotWoody.WoodyStates.state_cmd_user_list_choice_user, Command(commands=['cancel']))
@router.message(BotWoody.WoodyStatesTask.state_wait_choice, Command(commands=['cancel']))
@router.message(BotWoody.WoodyStatesTask.state_wait_user, Command(commands=['cancel']))
@router.message(BotWoody.WoodyStatesTask.state_wait_user_for_add, Command(commands=['cancel']))
@router.message(BotWoody.WoodyStatesTask.state_wait_user_del_yes_no, Command(commands=['cancel']))
async def cmd_get_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=BOT_LANG['/user cancel'], reply_markup=ReplyKeyboardRemove())
