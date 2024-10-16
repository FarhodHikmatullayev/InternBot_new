from aiogram.dispatcher.filters.state import StatesGroup, State


class DepartmentState(StatesGroup):
    department_id = State()
    name = State()


class CreateDepartmentState(StatesGroup):
    name = State()
    chief_id = State()


class UpdateDepartmentState(StatesGroup):
    department_id = State()
    name = State()


class DeleteDepartmentState(StatesGroup):
    department_id = State()
    name = State()
