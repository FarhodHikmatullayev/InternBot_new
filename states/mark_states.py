from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateMarkState(StatesGroup):
    intern_id = State()
    muomala = State()
    kirishimlilik = State()
    chaqqonlik_va_malaka = State()
    masuliyat = State()
    ozlashtirish_qobiliyati = State()
    ichki_tartibga_rioyasi = State()
    shaxsiy_intizomi = State()
    description = State()
    teacher_id = State()
    hr_id = State()
    chief_id = State()