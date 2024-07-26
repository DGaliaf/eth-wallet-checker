from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    user_seed = State()
    user_wallet = State()