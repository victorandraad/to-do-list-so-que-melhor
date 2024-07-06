from flet import *
from app.models.Database import Database
from app.models.Deck import Deck
from app.models.Task import Task

class TaskContainer(Container):
    def __init__(self):
        super().__init__()
        self.tasks: list = []
        self.width= 355
        self.height=234
        self.padding=padding.only(left=20)
        self.content=Column(
            scroll=ScrollMode.ADAPTIVE,
            controls=self.tasks
        )

        self.db: Database
        self.deck: Deck

    def update(self, e=False):
        self.tasks.clear()
        tasks = self.get_all_tasks()
        for task in tasks:
            tasked = self.to_task(task)
            tasked_row = self.to_row(tasked)
            self.tasks.insert(0, tasked_row)
        
        self.content.update()
        return super().update()
    
    def get_all_tasks(self):
        self.db.deck_name = self.deck.name
        return self.db.find_tasks()
    
    def to_task(self, task) -> list:
        return Task(
            name = task['name'],
            status = task['status'],
            sound = task['sound'],
            time = task['time'],
            break_time = task['break_time'],
            cycles = task['cycles'],
        )
    
    def to_row(self, task) -> Row:
        return TaskRow(self.db, task)


class TaskRow(Row):
    def __init__(self, db: Database, task: Task) -> None:
        super().__init__()

        self.task: Task = task
        self.db: Database = db

        self.status = [
            icons.CHECK_BOX_OUTLINE_BLANK, # nao feito  - 0 
            icons.RADIO_BUTTON_CHECKED, # fazendo  - 1 
            icons.FREE_BREAKFAST, # break  - 2 
            icons.PAUSE_ROUNDED, # pause  - 3 
            icons.CHECK_BOX # finished  - 4 
        ]

        self.icon_status = IconButton(
            icon=self.status[self.task.status],
            icon_color="#7094ff",
            on_click=self.change_status
        )

        self.alignment=MainAxisAlignment.SPACE_BETWEEN,
        self.controls=[
            Row(
                controls=[
                    self.icon_status,
                    Row(
                        controls=[Text(value=self.task.name, font_family="Roboto", color='white', width=250)],
                    )
                ]
            ),

            IconButton(icons.DELETE, width=30, height=30, icon_size=15, icon_color='red', on_click=self.delete_task)
        ]
    
    def delete_task(self, e):
        self.db.delete_task(self.task)
        self.visible = False
        self.update()

    def change_status(self, e):
        self.task.click()
        self.icon_status.icon = self.status[self.task.status]
        self.icon_status.update()
        self.update()