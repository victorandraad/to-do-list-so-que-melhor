from app.models.Database import Database
from app.models.Deck import Deck
from app.pages.createdeck import *
from app.pages.homepage import *
from flet import *


db = Database()

db.deck_name = 'deck temporário'

temporary_deck = Deck(
    'deck temporário',
    100,
    100,
    1,
    'app/assets/rings/alert-sound-loop-189741.mp3'
)

def main(page: Page):
    page.fonts = {
        "Roboto": "/fonts/Roboto-Regular.ttf",
    }
    page.route = "/"
    page.title = "TOMODORO"
    page.window_bgcolor = colors.TRANSPARENT
    page.bgcolor = colors.TRANSPARENT
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_left = 400
    page.window_top = 200
    page.window_width = 425
    page.window_height = 450
    
    def route_change(e: RouteChangeEvent):
        page.views.clear()
        if page.route == "/":
            homepage = HomePage(db, temporary_deck, page)
            homepage.db = db
            homepage.deck = temporary_deck

            page.views.append(homepage)
            page.update()
            homepage.decks_menu.updateDeck(db.deck_name)
            homepage.decks_menu.update_menu_items()
            homepage.decks_menu.update()
            homepage.task_container.update()

        if page.route == "/createdeck":
            create_deck_page = CreateDeckPage(db, page)
            create_deck_page.db = db

            page.views.append(create_deck_page)
            page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    app(target=main)
