"""
Inline-клавиатуры и CallbackData для чистой маршрутизации.
"""

from __future__ import annotations

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ActionCb(CallbackData, prefix="act"):
    action: str


class AgeCb(CallbackData, prefix="age"):
    value: int


class CardCb(CallbackData, prefix="card"):
    code: str


def start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡Далее",
                    callback_data=ActionCb(action="next").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Не нравиться",
                    callback_data=ActionCb(action="dislike").pack(),
                )
            ],
        ]
    )


def back_to_start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="На старт",
                    callback_data=ActionCb(action="to_start").pack(),
                )
            ]
        ]
    )


def proceed_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Приступить к заработку",
                    callback_data=ActionCb(action="proceed").pack(),
                )
            ]
        ]
    )


def age_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="+14", callback_data=AgeCb(value=14).pack()),
                InlineKeyboardButton(text="+18", callback_data=AgeCb(value=18).pack()),
            ]
        ]
    )


def cards_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Карта Альфа 1000р",
                    callback_data=CardCb(code="alfa_1000").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Карта Т-банк 500р",
                    callback_data=CardCb(code="tbank_500").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Карта озон 300р",
                    callback_data=CardCb(code="ozon_300").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отобразить карты для +18",
                    callback_data=ActionCb(action="show_18_cards").pack(),
                )
            ],
        ]
    )


def cards18_kb() -> InlineKeyboardMarkup:
    # Минимум 2 кнопки-заглушки по ТЗ
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Карта 18+ #1",
                    callback_data=CardCb(code="18_stub_1").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Карта 18+ #2",
                    callback_data=CardCb(code="18_stub_2").pack(),
                )
            ],
        ]
    )

