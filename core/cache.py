import requests
import Queue
import threading
import time

class Cache:

    cached_deck_page = {}
    q = Queue.Queue()
    
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def retry_request(url, params=None,  max_retry=3):
        for i in range(0, max_retry):
            try:
                cards_res = (requests.get(url, timeout=5)).json()
                cards = cards_res.get('cards')
                return cards
            except requests.exceptions.Timeout:
                pass
        return []

    def cache_single_page(self, username):
        get_decks_url = "http://0.0.0.0:8000/users/%s/decks"%username
        r = requests.get(get_decks_url)
        decks_res = r.json()
        decks =  decks_res.get('decks')
        timeout_decks = {}
        deck_idx = 0
        if decks != None:
            for deck in decks:
                deck_id = deck.get('id')
                get_cards_url = "http://0.0.0.0:8000/decks/%s"%deck_id
                try:
                    cards_res = (requests.get(get_cards_url, timeout=5)).json()
                    cards = cards_res.get('cards')
                    deck['cards'] = cards
                except requests.exceptions.Timeout:
                    timeout_decks[deck_idx] = get_cards_url
                deck_idx += 1
    
        for idx,url in timeout_decks.iteritems():
            decks[idx] = self.retry_request(url)
        return decks_res

    def run(self):
        while True:
            while not self.q.empty():
                username = self.q.get()
                r = self.cache_single_page(username)
                if self.cached_deck_page.get(username) == None:
                    self.cached_deck_page[username] = Queue.Queue()
                self.cached_deck_page[username].put(r)
            time.sleep(1000)
