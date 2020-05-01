import json
import re
import sqlite3
import os
from urllib.request import urlopen


with urlopen("https://shadowverse-portal.com/api/v1/cards?format=json&lang=en") as response:
    source = response.read()

cards_json = json.loads(source)
cards_iterator = filter(lambda card: card['card_name'] is not None, cards_json['data']['cards'])
cards = list(cards_iterator)


def replace_text(text):
    br = re.compile('<br>')
    line = re.compile('----------')

    text = re.sub(br, '\n', text)
    text = re.sub(line, '─────────', text)

    return text


for card in cards:
    card['card_name'] = card['card_name'].replace('\\', '').strip()
    card['description'] = replace_text(card['description'])
    card['evo_description'] = replace_text(card['evo_description'])


database_path = 'card_database.db'

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


def insert_card(card):
    with conn:
        c.execute("""INSERT INTO cards VALUES (:card_id,
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


print('inserting cards.')
for index, card in enumerate(cards):
    insert_card(card)
    print(str(index + 1) + ' out of ' + str(len(cards)) + ' cards. ')

conn.close()







