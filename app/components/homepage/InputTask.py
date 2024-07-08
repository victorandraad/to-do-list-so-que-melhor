from flet import *
from app.models.Database import Database
from app.models.Task import Task
from app.models.Deck import Deck

class InputTask(Container):
    def __init__(self):
        super().__init__()
        self.padding = padding.all(20)

        self.db: Database
        self.deck: Deck
        self.task_container: Container

        self.new_task = TextField(
            label="Escreva sua próxima tarefa",
            width=272,
            height=43, 
            color='white',
            on_submit=self.create_task
        )

        self.content = Row(
            alignment=MainAxisAlignment.START,
            controls=[
                self.new_task,
                IconButton(icons.CHECK, width=40, height=43, icon_color='white', on_click=self.create_task)
            ]
        )
    
    def create_task(self, e):
        if self.new_task.value == '':
            self.new_task.error_text = 'Nao pode ser vazio'
        else:
            self.new_task.error_text = ''
            task = Task(
                    name        = self.new_task.value,
                    time        = self.deck.time,
                    status      = 0,
                    break_time  = self.deck.break_time,
                    cycles      = self.deck.cycles,
                    sound       = self.deck.sound
            )
            self.db.create_task(task)

            self.new_task.value = ''

        self.deck.tasks = self.db.find_tasks()
        self.update()
        task = self.task_container.to_row(task)
        self.task_container.queue_tasks.append(task)
        self.task_container.update()
        self.new_task.focus()
        