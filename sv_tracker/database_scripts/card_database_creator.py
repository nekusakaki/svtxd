import json
import re
import sqlite3
import os
from urllib.request import urlopen
from urllib.error import *

DATABASE_PATH = 'database/card_database.db'


def create_card_database(print_function):
    print_function('Accessing website.')
    try:
        with urlopen("https://shadowverse-portal.com/api/v1/cards?format=json&lang=en") as response:
            source = response.read()
    except TimeoutError:
        print_function('Failed to access website. Update database to try again.')
        return
    except URLError:
        print_function('Failed to access website. Please check internet connection.')
        return

    print_function('Filtering cards.')
    cards_json = json.loads(source)
    cards_iterator = filter(lambda _card: _card['card_name'] is not None, cards_json['data']['cards'])
    cards = list(cards_iterator)

    for card in cards:
        card['card_name'] = card['card_name'].replace('\\', '').strip()
        card['description'] = replace_text(card['description'])
        card['evo_description'] = replace_text(card['evo_description'])

    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
        except OSError as e:
            print('Error while deleting file', DATABASE_PATH)
            print(e)

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    print_function('Creating table.')

    c.execute("""CREATE TABLE cards (
                    card_id integer,
                    card_set_id integer,
                    card_name text,
                    char_type integer,
                    clan integer,
                    tribe_name text,
                    skill_disc text,
                    evo_skill_disc text,
                    cost integer,
                    atk integer,
                    life integer,
                    evo_atk integer,
                    evo_life integer,
                    rarity integer,
                    use_red_ether integer,
                    description text,
                    evo_description text
                    )""")

    conn.commit()

    print_function('Inserting cards.')
    for index, card in enumerate(cards):
        insert_card(card, conn, c)
        print_function('Inserted ' + str(index + 1) + ' out of ' + str(len(cards)) + ' cards.')

    print_function('Completed.')

    conn.close()


def update_card_database(print_function):
    if not os.path.exists(DATABASE_PATH):
        create_card_database(print_function)
        return

    print_function('Accessing website.')
    try:
        with urlopen("https://shadowverse-portal.com/api/v1/cards?format=json&lang=en") as response:
            source = response.read()
    except TimeoutError:
        print_function('Failed to access website. Update database to try again.')
        return
    except URLError:
        print_function('Failed to access website. Please check internet connection.')
        return

    print_function('Filtering cards.')
    cards_json = json.loads(source)
    cards_iterator = filter(lambda _card: _card['card_name'] is not None, cards_json['data']['cards'])
    cards = list(cards_iterator)

    for card in cards:
        card['card_name'] = card['card_name'].replace('\\', '').strip()
        card['description'] = replace_text(card['description'])
        card['evo_description'] = replace_text(card['evo_description'])

    conn = sqlite3.connect(DATABASE_PATH)
    print_function('Retrieving Card IDs.')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    card_ids = c.execute('SELECT card_id FROM cards').fetchall()
    num_of_cards = len(cards)

    print_function('Inserting cards.')
    for index, card in enumerate(cards):
        if card['card_id'] not in card_ids:
            insert_card(card, conn, c)

        print_function('Inserted ' + str(index + 1) + ' out of ' + str(num_of_cards) + ' cards.')

    print_function('Completed.')

    conn.close()


def replace_text(text):
    br = re.compile('<br>')
    line = re.compile('----------')

    text = re.sub(br, '\n', text)
    text = re.sub(line, '─────────', text)

    return text


def insert_card(card, conn, cursor):
    with conn:
        cursor.execute("""INSERT INTO cards VALUES (:card_id,
            :card_set_id,
            :card_name,
            :char_type,
            :clan,
            :tribe_name,
            :skill_disc,
            :evo_skill_disc,
            :cost,
            :atk,
            :life,
            :evo_atk,
            :evo_life,
            :rarity,
            :use_red_ether,
            :description,
            :evo_description)""",
              {
                'card_id': card['card_id'],
                'card_set_id': card['card_set_id'],
                'card_name': card['card_name'],
                'char_type': card['char_type'],
                'clan': card['clan'],
                'tribe_name': card['tribe_name'],
                'skill_disc': card['skill_disc'],
                'evo_skill_disc': card['evo_skill_disc'],
                'cost': card['cost'],
                'atk': card['atk'],
                'life': card['life'],
                'evo_atk': card['evo_atk'],
                'evo_life': card['evo_life'],
                'rarity': card['rarity'],
                'use_red_ether': card['use_red_ether'],
                'description': card['description'],
                'evo_description': card['evo_description']
              })
