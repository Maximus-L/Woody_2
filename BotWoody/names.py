from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State

import Lib

bot: Bot
data_storages: [Lib.DLStore]


class WoodyStates(StatesGroup):
    state_cmd_list = State()
    state_cmd_help = State()
    state_cmd_get = State()
    state_cmd_get_filechoice = State()
