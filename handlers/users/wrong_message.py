from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state="*")
async def message_handler(message: types.Message):
    await message.answer("Notog'ri buyruq berdingiz!")
