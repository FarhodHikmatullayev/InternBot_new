from aiogram.dispatcher.filters.state import StatesGroup, State

class CreateChiefProfileState(StatesGroup):
    department_id = State()
    user_id = State()

class DeleteChiefProfileState(StatesGroup):
    department_id = State()
    profile_id = State()
    user_id = State()