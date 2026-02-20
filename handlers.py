from __future__ import annotations

import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import (
    PHOTO_1,
    PHOTO_2,
    PHOTO_3,
    PHOTO_4,
    PHOTO_5,
    PHOTO_6,
    SEND_DELAY_SECONDS,
)
from keyboards import (
    ActionCb,
    AgeCb,
    CardCb,
    age_kb,
    back_to_start_kb,
    cards18_kb,
    cards_kb,
    proceed_kb,
    start_kb,
)
from states import FunnelStates
from texts import (
    AGE_ASK_TEXT,
    CARDS_TEXT,
    DISLIKE_REPLY_TEXT,
    LINK_PLACEHOLDER_TEXT,
    ONLY_18_PLUS_TEXT,
    STALE_BUTTON_TEXT,
    START_TEXT,
    STEP1_MSG1_TEXT,
    STEP1_MSG2_TEXT,
    STEP1_MSG3_TEXT,
)


router = Router()


async def _send_start_screen(message: Message, state: FSMContext) -> None:
    """
    Показывает стартовый экран и переводит пользователя в состояние start_screen.
    """
    await state.clear()
    await message.answer_photo(
        photo=PHOTO_1,
        caption=START_TEXT,
        reply_markup=start_kb(),
    )
    await state.set_state(FunnelStates.start_screen)


async def _ensure_state_or_stale(
    state: FSMContext,
    expected_state: FunnelStates,
    callback: CallbackQuery,
) -> bool:
    """
    Проверка, что текущее состояние совпадает с ожидаемым.
    Если нет — шлём уведомление о «старой» кнопке и возвращаем False.
    """
    current = await state.get_state()
    if current != expected_state.state:
        await callback.answer(STALE_BUTTON_TEXT, show_alert=True)
        return False
    return True


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Команда /start — стартовый экран воронки.
    """
    await _send_start_screen(message, state)


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext) -> None:
    """
    Универсальная команда /menu — возвращает пользователя в стартовый экран.
    """
    await _send_start_screen(message, state)


@router.callback_query(ActionCb.filter(F.action == "to_start"))
async def cb_to_start(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ActionCb,
) -> None:
    """
    Кнопка «На старт» — всегда возвращает к начальному экрану.
    """
    del callback_data  # не используется
    if callback.message:
        await _send_start_screen(callback.message, state)
    await callback.answer()


@router.callback_query(ActionCb.filter(F.action == "dislike"))
async def cb_dislike(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ActionCb,
) -> None:
    """
    Кнопка «Не нравиться» на стартовом экране.
    """
    del callback_data
    if not await _ensure_state_or_stale(state, FunnelStates.start_screen, callback):
        return

    if callback.message:
        await callback.message.answer(
            DISLIKE_REPLY_TEXT,
            reply_markup=back_to_start_kb(),
        )
    await callback.answer()


@router.callback_query(ActionCb.filter(F.action == "next"))
async def cb_next(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ActionCb,
) -> None:
    """
    Кнопка «➡Далее»:
    отправляем 3 сообщения с картинками подряд с паузой 0.5 сек.
    """
    del callback_data
    if not await _ensure_state_or_stale(state, FunnelStates.start_screen, callback):
        return

    if not callback.message:
        await callback.answer()
        return

    # Сообщение 1
    await callback.message.answer_photo(
        photo=PHOTO_2,
        caption=STEP1_MSG1_TEXT,
    )

    await asyncio.sleep(SEND_DELAY_SECONDS)

    # Сообщение 2
    await callback.message.answer_photo(
        photo=PHOTO_3,
        caption=STEP1_MSG2_TEXT,
    )

    await asyncio.sleep(SEND_DELAY_SECONDS)

    # Сообщение 3 с кнопкой «Приступить к заработку»
    await callback.message.answer_photo(
        photo=PHOTO_4,
        caption=STEP1_MSG3_TEXT,
        reply_markup=proceed_kb(),
    )

    await state.set_state(FunnelStates.step1_done)
    await callback.answer()


@router.callback_query(ActionCb.filter(F.action == "proceed"))
async def cb_proceed(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ActionCb,
) -> None:
    """
    Кнопка «Приступить к заработку» после трёх сообщений.
    """
    del callback_data
    if not await _ensure_state_or_stale(state, FunnelStates.step1_done, callback):
        return

    if callback.message:
        await callback.message.answer_photo(
            photo=PHOTO_5,
            caption=AGE_ASK_TEXT,
            reply_markup=age_kb(),
        )

    await state.set_state(FunnelStates.age_choose)
    await callback.answer()


@router.callback_query(AgeCb.filter())
async def cb_age_choose(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: AgeCb,
) -> None:
    """
    Выбор возраста (+14 или +18).
    """
    if not await _ensure_state_or_stale(state, FunnelStates.age_choose, callback):
        return

    await state.update_data(age=callback_data.value)

    if callback.message:
        await callback.message.answer_photo(
            photo=PHOTO_6,
            caption=CARDS_TEXT,
            reply_markup=cards_kb(),
        )

    await state.set_state(FunnelStates.cards)
    await callback.answer()


@router.callback_query(CardCb.filter())
async def cb_card(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CardCb,
) -> None:
    """
    Обработка нажатия любой карты:
    отправляем заглушку с текстом ссылки.
    """
    del callback_data
    if not await _ensure_state_or_stale(state, FunnelStates.cards, callback):
        return

    if callback.message:
        await callback.message.answer(LINK_PLACEHOLDER_TEXT)
    await callback.answer()


@router.callback_query(ActionCb.filter(F.action == "show_18_cards"))
async def cb_show_18_cards(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: ActionCb,
) -> None:
    """
    Кнопка «Отобразить карты для +18».
    """
    del callback_data
    if not await _ensure_state_or_stale(state, FunnelStates.cards, callback):
        return

    data = await state.get_data()
    age = data.get("age")

    if callback.message:
        if age == 18:
            await callback.message.answer(
                "Дополнительные карты для 18+:",
                reply_markup=cards18_kb(),
            )
        else:
            await callback.message.answer(ONLY_18_PLUS_TEXT)

    await callback.answer()

