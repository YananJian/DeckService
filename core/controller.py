import sys
import os
from core.utils import Util
from core.cache import Cache
from django.http import HttpResponse
from django.http import JsonResponse
import requests
import Queue
working_dir = os.path.realpath(os.path.dirname(__file__) + '/../')
sys.path.append(working_dir) 

def get_decks(request, username):
    params = request.GET
    if params.get('reset'):
        Util.next_pageToken = 0
    if Util.next_pageToken != -1:
        response = JsonResponse(Util.all_res[Util.next_pageToken])
        Util.next_pageToken = Util.all_res[Util.next_pageToken].get('nextPageToken')
    else:
        response = JsonResponse({})
    return response

def get_specified_deck(request, deckid):
    print deckid
    res = {}
    res["id"] = deckid
    res["desc"] = Util.deck_id_desc_mapping.get(deckid)
    if res["desc"] == None:
        # Did not find the deck
        return JsonResponse({})
    res["cards"] = Util.generate_cards(deckid)
    response = JsonResponse(res)
    return response

def retry_request(url, params=None,  max_retry=3):
    for i in range(0, max_retry):
        try:
            cards_res = (requests.get(url, timeout=5)).json()
            cards = cards_res.get('cards')
            return cards
        except requests.exceptions.Timeout:
            pass
    return []

def get_detailed_decks(request, username):
    params = request.GET
    if not params.get('reset'):
        deck_detailed_queue = Cache.cached_deck_page.get(username) 
        if deck_detailed_queue != None:
            deck_detailed = deck_detailed_queue.get()
            if deck_detailed != None:
                print 'Cached...'
                response = JsonResponse(deck_detailed)
                if deck_detailed.get("nextPageToken") != -1:
                    Cache.q.put(username)
                return response

    get_decks_url = "http://0.0.0.0:8000/users/%s/decks"%username
    r = requests.get(get_decks_url, params=params)
    decks_res = r.json()
    decks =  decks_res.get('decks')
    # We have to keep good user experience, timeout is annoying
    # Don't keep long wait time, fetch all the other decks for now. Retry later.
    # If still timeout after retry, return empty list of cards
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
        decks[idx] = retry_request(url)
    if decks_res != {}:
        Cache.q.put(username)
    response = JsonResponse(decks_res)
    return response
