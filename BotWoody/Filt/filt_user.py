# -*- coding: utf-8 -*-

from aiogram.filters import BaseFilter
from aiogram.types import Message


class Users(BaseFilter):
    def __init__(self, src: str):
        self.source_name = src

    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        return False
