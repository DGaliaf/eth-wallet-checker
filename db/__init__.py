from typing import AnyStr


class Database:
    def __init__(self, db_path: str):
        self._db_path = db_path

        self.__users: set[str] = set()

        self.__init_db()

    def __init_db(self) -> None:
        with open(self._db_path, "r", encoding="utf-8") as connection:
            for user in connection:
                self.__users.add(user)

    def insert_temp(self, id: int) -> None:
        self.__users.add(str(id))

    def insert(self, data: str | int):
        with open(self._db_path, "r", encoding="utf-8") as connection:
            connection.write(str(f"{data}\n"))

    def read(self) -> AnyStr:
        with open(self._db_path, 'r') as connection:
            return connection.read()

