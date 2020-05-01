import sqlite3


class DatabaseInterface:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._conn = sqlite3.connect('card_database.db')
        self._c = self._conn.cursor()

    def get_card(self, card_id):
        self._c.execute('SELECT * FROM cards WHERE card_id=:card_id', {'card_id': card_id})
        return self._c.fetchone()




