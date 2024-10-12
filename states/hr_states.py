from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateHrProfileState(StatesGroup):
    user_id = State()

class DeleteHrProfileState(StatesGroup):
    user_id = State()
    profile_id = State()