from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.keyboards import start
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!"
                         f"\nMa'lumotlarni yuklashdan oldin boshlash tugmasini bosing⬇️", reply_markup=start)
