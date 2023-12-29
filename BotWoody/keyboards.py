# -*- coding: utf-8 -*-
import asyncio

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Клавиши да нет
def keyboard_yes_no() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


# ссылки на страницы с данными
def keyboard_url_data(urls: dict, url_key) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for url_name in urls.keys():
        kb.row(types.InlineKeyboardButton(
            text=url_name,
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


def inline_keyboard_cb_data(keys: [list]) -> InlineKeyboardMarkup:
    kb = []
    for key in keys:
        kb.append(InlineKeyboardButton(text=key[0], callback_data=key[1]))
    markup = InlineKeyboardMarkup(inline_keyboard=[kb])
    return markup


