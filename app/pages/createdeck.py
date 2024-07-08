from flet import *
from app.models.Database import Database
from app.models.Deck import Deck
from app.components.createdeckpage.TaskTimeField import TaskTimeField
from app.components.createdeckpage.CyclesField import CyclesField
from app.components.createdeckpage.RingField import RingField
from app.components.createdeckpage.DeckNameField import DeckNameField
from app.components.createdeckpage.BreakTimeField import BreakTimeField
from app.components.WindowControls import WindowControls
import os
import shutil

class CreateDeckPage(Container):
    def __init__(self, db: Deck, page: Page):
        super().__init__()
        self.border_radius = 10
        self.bgcolor = 'black'

        self.width = 425
        self.height = 440

        self.db = db
        self.page = page
        self.window_controls = WindowControls(self.page)
        self.deck_name_field = DeckNameField()
        self.task_time_field = TaskTimeField()
        self.break_time_field = BreakTimeField()
        self.cycles_field = CyclesField()
        self.ring_field = RingField()

        self.vertical_alignment = MainAxisAlignment.SPACE_BETWEEN

        self.deck_name_field.text_field.on_submit = self.create_deck
        self.task_time_field.task_time.on_submit = self.create_deck
        self.break_time_field.break_time.on_submit = self.create_deck
        self.cycles_field.cycles.on_submit = self.create_deck
        self.ring_field.selected_files.on_submit = self.create_deck

        self.content = Column(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.window_controls,
                self.deck_name_field,
                self.task_time_field,
                self.break_time_field,
                self.cycles_field,
                self.ring_field,
                self.footer(),
            ]
        )

    def footer(self):
        return Container(
            padding=20,
            content=Row(
                alignment=MainAxisAlignment.END,
                vertical_alignment=VerticalAlignment.END,
                controls=[
                    ElevatedButton("Cancelar", on_click= lambda _: self.page.go("/")),
                    ElevatedButton("Criar", on_click=self.create_deck)
                ]
            )
        )

    def create_deck(self, e):
        if self.deck_name_field.validade_deck_name():
            os.makedirs('app/assets/rings', exist_ok=True)

            ring_path = f'app/assets/rings/{self.ring_field.selected_files.value}'

            if not os.path.exists(ring_path):
                shutil.copy(self.ring_field.path, ring_path)

            deck = Deck(
                self.deck_name_field.text_field.value, 
                int(self.task_time_field.task_time.value) * 60, 
                int(self.break_time_field.break_time.value) * 60, 
                int(self.cycles_field.cycles.value), 
                ring_path
            )

            self.db.deck_name = deck.name
            self.db.create_deck(deck)
            self.page.go("/")