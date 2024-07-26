from aiogram import types

main_inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Согласен", callback_data="ok")]
])