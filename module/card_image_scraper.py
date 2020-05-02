import urllib.request
import sqlite3


def dl_card_jpg(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


conn = sqlite3.connect('card_database.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
card_ids = c.execute('SELECT card_id FROM cards').fetchall()
num_of_cards = len(card_ids)

for index, card_id in enumerate(card_ids):
    card_image_url = "https://shadowverse-portal.com/image/card/phase2/common/L/L_" + str(card_id) + ".jpg"
    images_path = "../images/"
    print("Downloading image " + str(index + 1) + " out of " + str(num_of_cards) + ".")
    dl_card_jpg(card_image_url, images_path, str(card_id))
