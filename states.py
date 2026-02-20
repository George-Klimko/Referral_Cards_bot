"""
FSM состояния воронки.
"""

from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class FunnelStates(StatesGroup):
    start_screen = State()
    step1_done = State()
    age_choose = State()
    cards = State()

