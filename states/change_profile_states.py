from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeProfileState(StatesGroup):
    user_id = State()
    first_name = State()
    last_name = State()
    phone_number = State()
