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

class CreateDeckPage(View):
    def __init__(self, db: Deck, page: Page):
        super().__init__()

        self.route = "/createdeck"
        self.bgcolor = 'black'
        self.db = db
        self.page = page
        self.window_controls = WindowControls(self.page)
        self.deck_name_field = DeckNameField()
        self.task_time_field = TaskTimeField()
        self.break_time_field = BreakTimeField()
        self.cycles_field = CyclesField()
        self.ring_field = RingField()

        self.deck_name_field.text_field.on_submit = self.create_deck
        self.task_time_field.task_time.on_submit = self.create_deck
        self.break_time_field.break_time.on_submit = self.create_deck
        self.cycles_field.cycles.on_submit = self.create_deck
        self.ring_field.selected_files.on_submit = self.create_deck

        self.controls = [
            self.window_controls,
            self.deck_name_field,
            self.task_time_field,
            self.break_time_field,
            self.cycles_field,
            self.footer()
        ]

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

            if not os.path.exists(f'app/assets/rings/{self.ring_field.selected_files.value}'):
                shutil.copy(self.ring_field.path, f'app/assets/rings/{self.ring_field.selected_files.value}')

            deck = Deck(
                self.deck_name_field.text_field.value, 
                self.task_time_field.task_time.value, 
                self.break_time_field.break_time.value, 
                self.cycles_field.cycles.value, 
                self.ring_field.selected_files.value
            )

            self.db.deck_name = deck.name
            self.db.create_deck(deck)
            self.page.go("/")