import sqlite3
import os

database_path = 'card_image_database.db'

if os.path.exists(database_path):
    try:
        os.remove(database_path)
    except OSError as e:
        print('Error while deleting file', database_path)
        print(e)

conn = sqlite3.connect(database_path)
c = conn.cursor()

print('Creating table.')

c.execute("""CREATE TABLE cards (
            card_id integer,
            card_image blob
          )""")

conn.commit()


def insert_card_image(card_id_number, card_image):
    with conn:
        c.execute("""INSERT INTO cards VALUES (
                    :card_id,
                    :card_image
                  )""",
                  {
                      'card_id': card_id_number,
                      'card_image': card_image
                  })


conn_card = sqlite3.connect('card_database.db')
conn_card.row_factory = lambda cursor, row: row[0]
c_card = conn_card.cursor()
card_ids = c_card.execute('SELECT card_id FROM cards').fetchall()
num_of_cards = len(card_ids)

for index, card_id in enumerate(card_ids):
    image_path = '../images/card_flair' + str(card_id) + '.jpg'
    with open(image_path, 'rb') as file:
        data = file.read()

    print('Inserting image ' + str(index + 1) + ' out of ' + str(num_of_cards) + '.')
    insert_card_image(card_id, data)
