from database_interface import DatabaseInterface


class Card:
    def __init__(self, card_id):
        self.card_id = card_id

        data = DatabaseInterface().get_card(card_id)

        if data:
            self.card_set_id = data[1]
            self.card_name = data[2]
            self.card_type = data[3]
            self.clan = data[4]
            self.trait = data[5]
            self.skill_disc = data[6]
            self.evo_skill = data[7]
            self.cost = data[8]
            self.atk = data[9]
            self.life = data[10]
            self.evo_atk = data[11]
            self.evo_life = data[12]
            self.rarity = data[13]
            self.vials = data[14]
            self.description = data[15]
            self.evo_description = data[16]
        else:
            raise ValueError('Invalid card id.')

    def __repr__(self):
        return f'{self.card_name}'


