from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    waiting_from = State()
    waiting_to = State()
    waiting_date = State()
    viewing_trains = State()
