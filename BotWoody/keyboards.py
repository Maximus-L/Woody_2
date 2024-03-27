# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import BotWoody.const as const


# Клавиши да нет
def keyboard_yes_no() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
            text='Да',
            callback_data='YES')
        )
    builder.add(types.InlineKeyboardButton(
            text='Нет',
            callback_data='NO')
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


# ссылки на страницы с данными
def keyboard_url_data(urls: dict, url_key) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for url_name in urls.keys():
        kb.row(types.InlineKeyboardButton(
            text=const.BOT_KEY_ICONS[2]+' '+urls[url_name]['description'],
            url=urls[url_name][url_key])
        )
    return kb.as_markup()


def reply_keyboard_src_data(keys: list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for key in keys:
        kb.button(text=key, callback_data=key)
    return kb.as_markup()


def inline_keyboard_src_data(keys: list) -> InlineKeyboardMarkup:
    kb = []
    for key in keys:
        kb.append(InlineKeyboardButton(text=key, callback_data=key))
    markup = InlineKeyboardMarkup(inline_keyboard=[kb])
    return markup


def reply_keyboard_cb_data(keys: [list]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for key in keys:
        kb.button(text=key[0]+'📁', callback_data=key[1])
    return kb.as_markup()


def inline_keyboard_cb_data(keys: [list], size=1, pict=0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for key in keys:
        builder.add(types.InlineKeyboardButton(
            text=const.BOT_KEY_ICONS[pict]+key[0],
            callback_data=key[1])
        )
    builder.adjust(size, repeat=True)
    return builder.as_markup()

