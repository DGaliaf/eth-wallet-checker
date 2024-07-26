from aiogram import Bot, Dispatcher, executor, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from bot.tg.utils import main_inline_keyboard, main_keyboard, UserState
from checker import Checker
from db import Database


class Bot:
    def __init__(self, db: Database, checker: Checker, config: dict):
        self._db: Database = db
        self._config: dict = config
        self._bot: Bot = Bot(self._config.get("bot_token"))

        self.__checker: Checker = checker

        self.__storage: MemoryStorage = MemoryStorage()
        self.__dp: Dispatcher = Dispatcher(self._bot, storage=self.__storage)


    async def welcome(self, message: types.Message):

        if not str(message.from_user.id) in self._db.read():
            self._db.insert(message.from_user.id)
            self._db.insert_temp(message.from_user.id)

            await message.answer('Правила:\n1. one\n2. two\n3. three', reply_markup=main_inline_keyboard)
        else:
            await message.answer('Приветствуем снова!', reply_markup=main_keyboard)

    @staticmethod
    async def st(call: types.CallbackQuery):
        await call.answer()
        await call.message.answer('Вас привествует бот от @BlazarPython. Используйте меню кнопок',
                                  reply_markup=main_keyboard)

    @staticmethod
    async def handlers(message: types.Message):
        if message.text == 'Проверка баланса эфира по адресу':
            await message.answer('Введите кошелёк.')
            await UserState.user_wallet.set()
        else:
            await message.answer('Используйте клавиатуру!!!')

    async def checker(self, message: types.Message, state: FSMContext):
        wallet = message.text
        if wallet[:2] == '0x':
            result = 'Баланс:'

            result += self.__checker.check_wallet(wallet)

            await message.answer(result)
            await state.clear()
        else:
            await message.answer('Неверный кошелёк.')

    def start(self):
        @self.__dp.message_handler(commands=['start', 'help'])
        async def wrapper_welcome(message: types.Message):
            await self.welcome(message)

        @self.__dp.callback_query_handler(text="ok")
        async def wrapper_start(call: types.CallbackQuery):
            await self.st(call)

        @self.__dp.message_handler(content_types=['text'])
        async def wrapper_handlers(message: types.Message):
            await self.handlers(message)

        @self.__dp.message_handler(state=UserState.user_wallet)
        async def wrapper_checker(message: types.Message, state: FSMContext):
            await self.checker(message, state)

        executor.start_polling(self.__dp, skip_updates=True)