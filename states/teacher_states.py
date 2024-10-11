from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateTeacherProfileState(StatesGroup):
    department_id = State()
    user_id = State()


class DeleteTeacherProfileState(StatesGroup):
    profile_id = State()
    department_id = State()
    user_id = State()
