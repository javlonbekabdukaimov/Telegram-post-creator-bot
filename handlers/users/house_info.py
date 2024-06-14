from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from keyboards.inline.keyboards import address, confirmation_keyboard, confirmation
from data.config import ADMINS, CHANNELS
from loader import dp, db, bot
from states.states import States

user_info = {
    "user_id": None,
    "photo_id": None,
    "address": None,
    "orientation": None,
    "price": None,
    "size": None,
    "no_of_rooms": None,
    "no_of_floors": None,
    "h_floor": None,
    "extra_info": None,
    "owner_phone": None,
    "caption": None,
    "mention": None
}

@dp.callback_query_handler(text=["start"], state="*")
async def start_test(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_info["user_id"] = call.from_user.id
    await call.message.answer("📸Uyingizning rasimini kiriting(rasm 1 tadan oshmasligi kerak):")
    await States.photo.set()

@dp.message_handler(state=States.photo, content_types=ContentType.PHOTO)
async def get_address(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    user_info["photo_id"] = photo_id
    await message.answer("📍Manzilni tanlang: ", reply_markup=address)
    await States.address.set()

@dp.callback_query_handler(text=["olmazor", "bektemir", "mirobod", "Mirzo-Ulug'bek", "sergeli", "chilonzor", "shayxontohur", "yunusobod", "yakkasaroy", "yashnabod"], state=States.address)
async def get_orientation(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    address = call.data
    user_info["address"] = address
    await call.message.answer("📍To'liq manzilni kiriting (masalan, Chilonzor tumani, Bunyodkor 3-a uy):")
    await States.orientation.set()

@dp.message_handler(state=States.orientation)
async def get_price(message: Message, state: FSMContext):
    orientation = message.text
    user_info["orientation"] = orientation
    await message.answer("💰Uyning narxini kiriting: ")
    await States.price.set()

@dp.message_handler(state=States.price)
async def get_size(message: Message, state: FSMContext):
    price = message.text
    user_info["price"] = price
    await message.answer("📏Uyning m\u00B2 kiriting: ")
    await States.size.set()

@dp.message_handler(state=States.size)
async def get_no_rooms(message: Message, state: FSMContext):
    size = message.text
    user_info["size"] = size
    await message.answer("🏢Xonalar sonini kiriting: ")
    await States.no_of_rooms.set()

@dp.message_handler(state=States.no_of_rooms)
async def get_no_floors(message: Message, state: FSMContext):
    no_of_rooms = message.text
    user_info["no_of_rooms"] = no_of_rooms
    await message.answer("🏢Domning qavatlari sonini kiriting: ")
    await States.no_of_floors.set()

@dp.message_handler(state=States.no_of_floors)
async def h_floor(message: Message, state: FSMContext):
    no_of_floors = message.text
    user_info["no_of_floors"] = no_of_floors
    await message.answer("🏢Uyning qavatini kiriting: ")
    await States.h_floor.set()

@dp.message_handler(state=States.h_floor)
async def h_floor(message: Message, state: FSMContext):
    h_floor = message.text
    user_info["h_floor"] = h_floor
    await message.answer("📋Qoshimcha ma'lumot kiriting (uyning sharoiti, jihozlari va h.k.): ")
    await States.extra_info.set()

@dp.message_handler(state=States.extra_info)
async def h_floor(message: Message, state: FSMContext):
    extra_info = message.text
    user_info["extra_info"] = extra_info
    await message.answer("📞Telefon raqamingizni kiriting: ")
    await States.owner_phone.set()

@dp.message_handler(state=States.owner_phone)
async def h_floor(message: Message, state: FSMContext):
    owner_phone = message.text
    user_info["owner_phone"] = owner_phone

    photo_id = user_info["photo_id"]
    address = user_info["address"]
    orientation = user_info["orientation"]
    price = user_info["price"]
    size = user_info["size"]
    no_of_rooms = user_info["no_of_rooms"]
    no_of_floors = user_info["no_of_floors"]
    h_floor = user_info["h_floor"]
    extra_info = user_info["extra_info"]
    owner_phone = user_info["owner_phone"]

    caption = (f"🆕{address.title()} tumanida kvartira sotiladi"
               f"\n\n📍To'liq manzil: {orientation}"
               f"\n🏢{no_of_floors} qavatli dom, {h_floor}-qavat"
               f"\n🏢{no_of_rooms} xona, {size}m\u00B2"
               f"\n💰Narxi: {price}$"
               f"\n✅Qo'shimcha ma'lumot: {extra_info}"
               f"\n\n📞Tel: {owner_phone}")

    user_info["caption"] = caption
    user_info["mention"] = message.from_user.get_mention()

    await message.answer_photo(photo_id, caption=caption, reply_markup=confirmation_keyboard)
    await States.send_to_admin.set()


@dp.callback_query_handler(text=['send_to_admin'], state=States.send_to_admin)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Post adminga yuborildi.")
    photo_id = user_info["photo_id"]
    caption = user_info["caption"]
    mention = user_info["mention"]
    await bot.send_message(ADMINS[0], f"📢Foydalanuvchi {mention} quyidagi postni chop etmoqchi:")
    await bot.send_photo(ADMINS[0], photo_id, caption=caption, reply_markup=confirmation)
    await States.post.set()

@dp.callback_query_handler(text=['post'], user_id=ADMINS, state="*")
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.answer("✅Postni kanalga joylashga ruhsat berdingiz.", show_alert=True)
    channel = CHANNELS[0]

    photo_id = user_info["photo_id"]
    caption = user_info["caption"]
    await bot.send_photo(chat_id=channel, photo=photo_id, caption=caption)

    user_id = user_info["user_id"]
    address = user_info["address"]
    orientation = user_info["orientation"]
    price = user_info["price"]
    size = user_info["size"]
    no_of_rooms = user_info["no_of_rooms"]
    no_of_floors = user_info["no_of_floors"]
    h_floor = user_info["h_floor"]
    extra_info = user_info["extra_info"]
    owner_phone = user_info["owner_phone"]
    await db.insert_info(user_id=user_id, address=address, orientation=orientation, price=price,
                         size=size, no_of_rooms=no_of_rooms, no_of_floors=no_of_floors, h_floor=h_floor,
                         extra_info=extra_info, owner_phone=owner_phone, photo_id=photo_id)
    await state.finish()


@dp.callback_query_handler(text=['cancel'], state=States.send_to_admin)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("❌Post rad etildi.")
    await state.finish()

@dp.callback_query_handler(text=['cancel'], user_id=ADMINS)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("❌Post rad etildi.")

    user_id = user_info["user_id"]
    await bot.send_message(user_id, "❌Post rad etildi.")
    await state.finish()
