from aiogram import types

main_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Мои кошельки")],
    [types.KeyboardButton(text='Добавить кошелек')],
    [types.KeyboardButton(text="Удалить кошелек")],
    [types.KeyboardButton(text='Проверка баланса эфира по адресу')],
], resize_keyboard=True)
