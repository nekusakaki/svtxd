import sqlite3

DATABASE_PATH = 'database/card_database.db'


class DatabaseInterface:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._conn = sqlite3.connect(DATABASE_PATH)
        self._c = self._conn.cursor()

    def __del__(self):
        self._c.close()
        self._conn.close()

    def get_card(self, card_id):
        self._c.execute('SELECT * FROM cards WHERE card_id=:card_id', {'card_id': card_id})
        card = self._c.fetchone()
        return card




