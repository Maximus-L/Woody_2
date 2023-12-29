# -*- coding: utf-8 -*-


from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext


import BotWoody
import Scaner

router = Router()


# /urls command
@router.message(Command(commands=['urls']))
async def cmd_urls_answer(message: Message, state: FSMContext):
    await message.answer(text='::', reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Ссылки на данные",
                         reply_markup=BotWoody.keyboard_url_data(
                            Scaner.DATA_SOURCE, url_key='url'))
    await state.clear()
