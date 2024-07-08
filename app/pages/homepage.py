from flet import *
from app.models.Deck import Deck
from app.models.Database import Database
from app.components.homepage.DecksMenu import DecksMenu
from app.components.homepage.InputTask import InputTask
from app.components.homepage.TaskContainer import TaskContainer
from app.components.WindowControls import WindowControls

class HomePage(Container):
    def __init__(self, db: Deck, deck: Database, page: Page):
        super().__init__()

        self.border_radius = 10
        self.bgcolor = 'black'
        
        self.width = 425
        self.height = 440

        self.deck = deck
        self.db = db
        self.page = page
        self.window_controls = WindowControls(self.page)
        self.task_container = TaskContainer()
        self.decks_menu = DecksMenu(self.page, self.db, self.task_container)

        self.input_container = InputTask()
        self.input_container.task_container = self.task_container

        self.window_controls.db = self.db

        self.task_container.db = self.db
        self.task_container.deck = self.deck
        self.decks_menu.deck = self.deck
        self.input_container.db = self.db
        self.input_container.deck = self.deck

        self.content = Column(
            controls=[
                self.window_controls,
                self.decks_menu,
                self.input_container,
                self.task_container,
            ]
        )