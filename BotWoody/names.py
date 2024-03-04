from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State

import Lib
import DbUsers
import redis

bot: Bot
data_storages: [Lib.DLStore]
db_users: DbUsers.DbProvider
r: redis.Redis


class WoodyStates(StatesGroup):
    state_cmd_list = State()
    state_cmd_help = State()
    state_cmd_get = State()
    state_cmd_get_filechoice = State()
    state_cmd_user = State()
    state_cmd_user_add = State()
    state_cmd_user_add_id = State()
    state_cmd_user_add_name = State()
