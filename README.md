# DeckService

####Implementation of auto-caching server and auto-retry upon timeout
-------
#### Requirements
> Django <br>
> Requests

-------
#### Run
<code> python manage.py runserver 0.0.0.0:8000 </code>

#### Try it out
<code> http://0.0.0.0:8000/users/abc/detailed_decks </code> <br>
<code> http://0.0.0.0:8000/users/abc/detailed_decks?reset=True </code>

-------
#### What did the server do
As we know, decks are collections of cards. This server mocks up card and deck generating.<br>
It implemented three routes:<br>
> GET /users/{username}/decks <br>
> GET /decks/{id}
> GET /users/{username}/detailed_decks <br>

The last route returns the detailed decks which uses the above two routes and combines together cards returned by the second route with collection of decks from the first route.<br>

If you keep on requesting 'GET /users/{username}/detailed_decks', it will give you incremental results (next page, page after next page etc. until it reaches the last page). <br>

You can also reset the page index, so that after hitting the last page, you can still go back to the first page.

-------
#### Files and what do they do
The core/ has three main files: cache.py, controller.py and utils.py.<br>
The deckService/ has file urls.py
-- utils.py mocks up data for global usage. <br>
-- cache.py has a daemon thread which pre-loads the next page given the current page. Note that since decks are paginated, the pageId of the last page is -1 (It's convinient for marking it as end of all pages).<br>
-- controller.py has all routes implemented.<br>
-- urls.py defines the routes and initializes data mockup and the background cache.







