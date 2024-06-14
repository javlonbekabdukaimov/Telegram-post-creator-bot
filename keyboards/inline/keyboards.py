from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Boshlash", callback_data="start")
        ],
    ],
)

address = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Olmazor", callback_data="olmazor")
        ],
        [
            InlineKeyboardButton(text="Bektemir", callback_data="bektemir")
        ],
        [
            InlineKeyboardButton(text="Mirobod", callback_data="mirobod")
        ],
        [
            InlineKeyboardButton(text="Mirzo-Ulug'bek", callback_data="Mirzo-Ulug'bek")
        ],
        [
            InlineKeyboardButton(text="Sergeli", callback_data="sergeli")
        ],
        [
            InlineKeyboardButton(text="Chilonzor", callback_data="chilonzor")
        ],
        [
            InlineKeyboardButton(text="Shayxontohur", callback_data="shayxontohur")
        ],
        [
            InlineKeyboardButton(text="Yunusobod", callback_data="yunusobod")
        ],
        [
            InlineKeyboardButton(text="Yakkasaroy", callback_data="yakkasaroy")
        ],
        [
            InlineKeyboardButton(text="Yashnabod", callback_data="yashnabod")
        ],
    ],
)

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Postni adminga yuborish", callback_data="send_to_admin")
        ],
        [
            InlineKeyboardButton(text="❌Rad etish", callback_data="cancel")
        ],
    ],
)

confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Postni kanalga joylash", callback_data="post")
        ],
        [
            InlineKeyboardButton(text="❌Rad etish", callback_data="cancel")
        ],
    ],
)

