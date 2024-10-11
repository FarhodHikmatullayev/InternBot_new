from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateInternState(StatesGroup):
    department_id = State()
    user_id = State()
    teacher_id = State()
    internship_period = State()

class DeleteInternState(StatesGroup):
    department_id = State()
    user_id = State()
    intern_id = State()