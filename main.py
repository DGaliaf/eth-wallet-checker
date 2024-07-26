from bot.tg import Bot
from checker import Checker
from config import CONFIG
from db import Database

if __name__ == "__main__":
    db = Database("user_ids.txt")
    checker = Checker()

    bot = Bot(db, checker, CONFIG)