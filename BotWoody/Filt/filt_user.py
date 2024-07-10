# -*- coding: utf-8 -*-

from aiogram.filters import Filter
from aiogram.types import Message
import BotWoody
from DbRedis import (R_PREFIX_PRIMARY, R_PREFIX_USER)


class UsersByRole(Filter):

    def __init__(self, roles: list | None = None) -> None:
        self.__roles = roles

    async def __call__(self, message: Message) -> bool:
        role = BotWoody.r.hget(R_PREFIX_PRIMARY + R_PREFIX_USER + str(message.from_user.id), 'role')
        if role is None:
            return False
        role = bytes.decode(role)
        return role in self.__roles


