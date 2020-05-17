import sqlite3
import os
import urllib.request
from urllib.error import *

DATABASE_PATH = 'database/card_image_database.db'


def create_card_image_database(print_function):
    print_function('Creating Database.')
    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
        except OSError as e:
            print('Error while deleting file', DATABASE_PATH)
            print(e)

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    print_function('Creating Table.')

    c.execute("""CREATE TABLE cards (
                card_id integer,
                card_image blob
              )""")

    conn.commit()

    print_function('Retrieving Card IDs.')
    conn_card = sqlite3.connect('database/card_database.db')
    conn_card.row_factory = lambda cursor, row: row[0]
    c_card = conn_card.cursor()
    card_ids = c_card.execute('SELECT card_id FROM cards').fetchall()
    num_of_cards = len(card_ids)

    print_function('Inserting Card Images.')
    for index, card_id in enumerate(card_ids):
        try:
            card_image_url = "https://shadowverse-portal.com/image/card/phase2/common/L/L_" + str(card_id) + ".jpg"
            with urllib.request.urlopen(card_image_url) as response:
                data = response.read()

            insert_card_image(card_id, data, conn, c)
        except TimeoutError:
            print_function('Downloading image failed. Update database to try again.')
            return
        except URLError:
            print_function('Unable to reach website. Please check internet connection.')
            return

        print_function('Inserted ' + str(index + 1) + ' out of ' + str(num_of_cards) + ' images.')

    print_function('Completed')
    conn.close()


def update_card_image_database(print_function):
    if not os.path.exists(DATABASE_PATH):
        create_card_image_database(print_function)
        return

    print_function('Accessing Database.')
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    image_card_ids = c.execute('SELECT card_id FROM cards').fetchall()

    print_function('Retrieving Card IDs.')
    conn_card = sqlite3.connect('database/card_database.db')
    conn_card.row_factory = lambda cursor, row: row[0]
    c_card = conn_card.cursor()
    card_card_ids = c_card.execute('SELECT card_id FROM cards').fetchall()
    num_of_cards = len(card_card_ids)

    print_function('Inserting Card Images.')
    for index, card_id in enumerate(card_card_ids):
        if card_id not in image_card_ids:
            try:
                card_image_url = "https://shadowverse-portal.com/image/card/phase2/common/L/L_" + str(card_id) + ".jpg"
                with urllib.request.urlopen(card_image_url) as response:
                    data = response.read()

                insert_card_image(card_id, data, conn, c)
            except TimeoutError:
                print_function('Downloading image failed. Update database to try again.')
                return
            except URLError:
                print_function('Unable to reach website. Please check internet connection.')
                return

        print_function('Inserted ' + str(index + 1) + ' out of ' + str(num_of_cards) + ' images.')

    print_function('Completed')
    conn.close()


def insert_card_image(card_id_number, card_image, conn, cursor):
    with conn:
        cursor.execute("""INSERT INTO cards VALUES (
                    :card_id,
                    :card_image
                  )""",
                  {
                      'card_id': card_id_number,
                      'card_image': card_image
                  })
