from aiogram.dispatcher.filters.state import StatesGroup, State


class DownloadMarkState(StatesGroup):
    intern_id = State()
    user_id = State()