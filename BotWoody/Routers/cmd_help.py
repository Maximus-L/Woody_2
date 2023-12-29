# -*- coding: utf-8 -*-
# Роутер по команде /help
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

import BotWoody.const as const

router = Router()


@router.message(Command(commands=['help']),
                F.from_user.id.in_(const.BOT_ADMINS))
async def cmd_help_answer_adm(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_ADM_COMMANDS:
        await message.answer(cmd_help)


@router.message(Command(commands=['help']),
                F.from_user.id.in_(const.BOT_USERS))
async def cmd_help_answer_user1(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_USER_COMMANDS:
        await message.answer(cmd_help)


@router.message(Command(commands=['help']),
                F.from_user.id.in_(const.BOT_OPERATORS))
async def cmd_help_answer_operator1(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    for cmd_help in const.BOT_HELP_OPERATOR_COMMANDS:
        await message.answer(cmd_help)


@router.message(Command(commands=['help']),
                )
async def cmd_help_answer_other(message: Message):
    await message.answer(text="Доступные команды:",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text="/help - список команд")
    await message.answer(text="/id - id пользователя")


@router.message(Command(commands=['id']),
                )
async def cmd_help_answer_other(message: Message):
    user_id = message.from_user.id
    await message.answer(text=f"Ваш ID: {user_id}",
                         reply_markup=ReplyKeyboardRemove())
