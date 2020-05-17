import sqlite3
import io

IMAGE_DATABASE_PATH = 'database/card_image_database.db'


class ImageDatabaseInterface:
    CARD_ID = 0
    CARD_IMAGE = 1

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._conn = sqlite3.connect(IMAGE_DATABASE_PATH)
        self._c = self._conn.cursor()

    def __del__(self):
        self._c.close()
        self._conn.close()

    def get_card_image(self, card_id):
        self._c.execute('SELECT * FROM cards WHERE card_id=:card_id', {'card_id': card_id})
        card = self._c.fetchone()
        return io.BytesIO(card[self.CARD_IMAGE])

