import random
import string

class Util:
    
    page_size= 10
    all_res = []
    deck_id_desc_mapping = {}
    next_pageToken = 0
    
    @staticmethod
    def generate_decks_per_page(size, current_pageid, next_pageid):
        decks = []
        existing_ids= set()
        res = {}
        id_digits = 5
        desc_digits = 6
        chars = string.ascii_uppercase + string.digits
        for i in range(0, size):
            deck = {}
            key = ''.join(random.choice(string.digits) for _ in range(id_digits))
            desc = ''.join(random.choice(chars) for _ in range(desc_digits)) 
            if key == existing_ids:
                i -= 1
                continue
            deck["id"] = key
            deck["desc"] = desc 
            Util.deck_id_desc_mapping[key] = desc
            decks.append(deck)
        res["decks"] = decks
        res["nextPageToken"] = next_pageid
        res["currentPageToken"] = current_pageid
        res["resultSizeEstimate"] = len(decks)
        return res

    @staticmethod
    def generate_decks_multi_pages(total_pages=10):
        Util.all_res = []
        for i in range(0, total_pages):
            if i == total_pages - 1:
                Util.all_res.append(Util.generate_decks_per_page(5, i, -1))
            else:
                Util.all_res.append(Util.generate_decks_per_page(5, i, i+1))

    @staticmethod
    def get_all_pages():
        return Util.all_res

    @staticmethod
    def get_page(pageToken):
        return Util.all_res[pageToken]

    @staticmethod
    def generate_cards(deckid):
        cards = []
        num_cards = 3
        id_digits = 4
        desc_digits = 6
        chars = string.ascii_uppercase + string.digits
        for i in range(0, num_cards):
            card = {}
            key = ''.join(random.choice(string.digits) for _ in range(id_digits)) 
            card["id"] = str(key)
            card["title"] = str(''.join(random.choice(chars) for _ in range(desc_digits))) 
            card["payload"] = {}
            cards.append(card)
        return cards


