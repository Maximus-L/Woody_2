# -*- coding: utf-8 -*-
# Роутер по команде /help
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

import BotWoody.const as const
import BotWoody.Filt as Filt

router = Router()


# Список команд для администратора
# @router.message(Command(commands=['help']),
#                 F.from_user.id.in_(const.BOT_ADMINS))
# @router.message(Command(commands=['help']),
#                 F.from_user.id.in_(DbRedis.get_users_by_role(['admin'])))
# @router.message(Command(commands=['help']), DbRedis.is_member_by_role(roles=['admin']))
@router.message(Command(commands=['help']), Filt.UsersByRole(roles=['admin']))
async def cmd_help_answer_adm(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_ADM_COMMANDS:
        await message.answer(cmd_help)


# Список команд для пользователя
# @router.message(Command(commands=['help']),
#                 F.from_user.id.in_(const.BOT_USERS))
# @router.message(Command(commands=['help']),
#                 F.from_user.id.in_(DbRedis.get_users_by_role(['admin'])))
@router.message(Command(commands=['help']), Filt.UsersByRole(roles=['user']))
async def cmd_help_answer_user1(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_USER_COMMANDS:
        await message.answer(cmd_help)


# Список команд для оператора
# @router.message(Command(commands=['help']),
#                 F.from_user.id.in_(const.BOT_OPERATORS))
@router.message(Command(commands=['help']), Filt.UsersByRole(roles=['operator']))
async def cmd_help_answer_operator1(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_OPERATOR_COMMANDS:
        await message.answer(cmd_help)


# Список команд для "остальных"
@router.message(Command(commands=['help']))
async def cmd_help_answer_other(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_GUEST_COMMANDS:
        await message.answer(cmd_help)


# Отображение ID пользователя
@router.message(Command(commands=['id']))
async def cmd_help_answer_other(message: Message):
    user_id = message.from_user.id
    await message.answer(text=f"Ваш ID: {user_id}",
                         reply_markup=ReplyKeyboardRemove())
