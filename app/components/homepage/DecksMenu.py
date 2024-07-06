from flet import *
from app.models.Database import Database
from app.models.Deck import Deck

class DecksMenu(Container):
    def __init__(self, page, db) -> None:
        super().__init__()

        self.deckname: str = 'deck temporário'
        self.menu_items: list = []

        self.db: Database = db
        self.deck: Deck
        self.task_container: Container

        self.page = page
        self.padding = padding.only(left=20, bottom=10, right=20)

        self.sub_menu = SubmenuButton(
            content = Text(self.deckname, color='white', size=20),
            controls = self.menu_items
        )

        self.content = MenuBar(
            expand =True,
            style = MenuStyle(
                alignment = alignment.center,
                bgcolor = colors.BLUE,
                mouse_cursor = {
                    MaterialState.HOVERED: MouseCursor.WAIT,
                    MaterialState.DEFAULT: MouseCursor.ZOOM_OUT
                },
            ),
            controls=[self.sub_menu]
        )

        self.update_menu_items()
        
    def updateDeck(self, new_deck_name: str):
        self.sub_menu.content.value = new_deck_name  # Atualiza o nome do deck

        self.db.deck_name = new_deck_name
        self.deck.name = self.db.deck_name

        self.db.create_deck(self.deck)

        self.deck.name, self.deck.time, self.deck.break_time, self.deck.sound, self.deck.cycles = self.db.find_deck()

        self.sub_menu.update()
        self.task_container.update()

    def delete_deck(self, deck):
        self.db.deck_name = deck
        self.db.delete_deck(deck)

        self.update_menu_items()
        self.update()

        if self.sub_menu.content.value == self.db.deck_name:
            self.db.deck_name = 'deck temporário'
            self.sub_menu.content.value = 'deck temporário'
            self.update_menu_items()
            self.update()
            self.task_container.tasks.clear()
            self.task_container.update()
            self.db.delete_deck(deck)

    def route_to_create_deck(self, e):
        self.page.go("/createdeck")

    def update_menu_items(self):
        self.menu_items.clear()
        decks = self.db.find_decks()
        for deck in decks:
            self.menu_items.append(
                Container(
                    padding=padding.all(10),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        
                        controls=[
                            MenuItemButton(
                                content=Text(deck),
                                leading=Icon(icons.FOLDER),
                                style=ButtonStyle(bgcolor={MaterialState.HOVERED: colors.GREEN}),
                                on_click=lambda e, deck=deck: self.updateDeck(deck),
                            ),

                            IconButton(icons.DELETE, width=30, height=30, icon_size=15, icon_color='red', on_click= lambda _, deck=deck: self.delete_deck(deck)), 
                        ]
                    )
                )
                
            )

        self.menu_items.append(
            MenuItemButton(
                content=Text("Criar novo deck."),
                leading=Icon(icons.CREATE_NEW_FOLDER),
                style=ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                on_click=self.route_to_create_deck
            )
        )
        