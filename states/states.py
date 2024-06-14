from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    photo = State()
    address = State()
    orientation = State()
    price = State()
    size = State()
    no_of_rooms = State()
    no_of_floors = State()
    h_floor = State()
    extra_info = State()
    owner_phone = State()
    send_to_admin = State()
    post = State()