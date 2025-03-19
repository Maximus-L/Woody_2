from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State
import redis
import Lib

r: redis.Redis

bot: Bot
data_storages: [Lib.DLStore]


class WoodyStates(StatesGroup):
    state_cmd_list = State()
    state_cmd_help = State()
    state_cmd_get = State()
    state_cmd_get_filechoice = State()
    state_cmd_user = State()
    state_cmd_user_add = State()
    state_cmd_user_add_id = State()
    state_cmd_user_add_name = State()
    state_cmd_user_list = State()
    state_cmd_user_list_choice_user = State()


class WoodyStatesUserEdit(StatesGroup):
    state_wait_edited_param = State()
    state_wait_value = State()
    state_wait_name = State()
    state_wait_role = State()


class WoodyStatesTask(StatesGroup):
    state_wait_choice = State()
    state_wait_user = State()
    state_wait_user_for_add = State()
    state_wait_user_del_yes_no = State()
