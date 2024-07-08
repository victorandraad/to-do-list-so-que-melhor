from flet import *
from app.models.Database import Database
from app.models.Deck import Deck
from app.models.Task import Task
from time import sleep

class TaskContainer(Container):
    def __init__(self):
        super().__init__()
        self.tasks: list = []
        self.queue_tasks: list = []
        self.width= 355
        self.height=234
        self.padding=padding.only(left=20)
        self.dialog_change_deck: AlertDialog = None

        self.content=Container(
            content=
                Column(
                    scroll=ScrollMode.ADAPTIVE,
                    controls=[
                        Column(
                            scroll=ScrollMode.ADAPTIVE,
                            controls=self.tasks
                        ),
                        Column(
                            scroll=ScrollMode.ADAPTIVE,
                            controls=self.queue_tasks
                        ),
                    ]
                )
        )

        self.db:Database
        self.deck: Deck

    def update(self, force=False):
        if not self.get_active_task(None) or force:
            self.queue_tasks.clear()
            self.tasks.clear()

            if self.dialog_change_deck != None:
                self.queue_tasks.append(self.dialog_change_deck) 
            
            tasks = self.get_all_tasks()
            for task in tasks:
                tasked = self.to_task(task)
                tasked_row = self.to_row(tasked)
                self.tasks.append(tasked_row)
            
            self.content.update()
            return super().update()
        
        self.content.content.controls[1].update()

        
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
        return TaskRow(self.db, task, self.deck, self.get_active_task)

    def get_active_task(self, task_name) -> bool:
        """
        False = no active tasks
        else: return task
        """
        for task in self.tasks:
            if task.controls[0].controls[0].icon != icons.CHECK_BOX_OUTLINE_BLANK:
                if task_name != task.controls[0].controls[1].controls[0].value:
                    return task.controls[0].controls[1].controls[0].value
        
        return False

class TaskRow(Row):
    def __init__(self, db: Database, task: Task, deck: Deck, get_active_task) -> None:
        super().__init__()

        self.task: Task = task
        self.db: Database = db
        self.deck: Deck = deck
        self.get_active_task = get_active_task

        self.status = [
            icons.CHECK_BOX_OUTLINE_BLANK, # nao feito  - 0 
            icons.RADIO_BUTTON_CHECKED, # fazendo  - 1 
            icons.FREE_BREAKFAST, # break  - 2 
            icons.PAUSE_ROUNDED, # pause  - 3 
            icons.CHECK_BOX # finished  - 4 
        ]

        self.dialog_start_another_task_error = AlertDialog(
            modal=True, 
            title=Text("Atenção!", color=colors.BLUE), 
            open=False,
            content=Text(value="Você deve terminar uma tarefa antes de começar outra."), 
            actions=[TextButton("Voltar.", on_click=self.decline_change, ),]
        )

        self.icon_status = IconButton(
            icon=self.status[self.task.status],
            icon_color="#7094ff",
            on_click=self.change_status_click
        )

        self.alignment=MainAxisAlignment.SPACE_BETWEEN,
        self.controls=[
            Row(
                width=250,
                controls=[
                    self.icon_status,
                    Row(
                        wrap=True,
                        controls=[Text(value=self.task.name, font_family="Roboto", color='white', width=200)],
                    )
                ]
            ),
            Text(value="00:00", color='black'),
            self.dialog_start_another_task_error,
            IconButton(icons.DELETE, width=30, height=30, icon_size=15, icon_color='red', on_click=self.delete_task),
            # Future finish task implementation
            # IconButton(icons.VERIFIED, width=30, height=30, icon_size=15, icon_color='GREEN')
        ]
    
    def decline_change(self, e):
        self.dialog_start_another_task_error.open = False
        self.update()

    def delete_task(self, e):
        self.db.delete_task(self.task)
        self.visible = False
        self.task.set_blank()
        self.icon_status.icon = self.status[0]
        self.update()

    def change_status(self):
        self.icon_status.icon = self.status[self.task.status]
        self.icon_status.update()
        self.set_timer()
        self.update()
        self.timer()   

    def change_status_click(self, e):
        active_task = self.get_active_task(self.task.name)
        if not active_task:
            self.task.click()
            self.change_status()
        
        else:
            self.dialog_start_another_task_error.open = True
            self.update()

        
    def set_timer(self):
        self.time_minutes, self.time_seconds = divmod(self.task.time, 60)
        self.break_time_minutes, self.break_time_seconds = divmod(self.task.break_time, 60)

        if not self.task.paused and not self.task.running and not self.task.is_break_time:
            self.controls[1].color =  'black'
        else:
            self.controls[1].color = 'white'

        if self.task.is_break_time:
            break_time_string = f'{self.break_time_minutes:02.0f}:{self.break_time_seconds:02.0f}'
            self.controls[1].value = break_time_string
        
        elif self.task.running:
            time_string = f'{self.time_minutes:02.0f}:{self.time_seconds:02.0f}'
            self.controls[1].value = time_string

    def time_decrease(self):
        self.task.time -= 1
    
    def break_time_decrease(self):
        self.task.break_time -= 1
    
    def timer(self):
        if self.task.running:
            for c in range(self.task.time):
                if not self.task.paused and not self.task.blank:
                    sleep(1)
                    self.time_decrease()
                    self.set_timer()
                    self.update()

                else:
                    break
            if self.task.time <= 0:
                self.task.cycles -= 1

                if self.task.cycles <= 0:
                    self.task.time = self.deck.time
                    self.task.cycles = self.deck.cycles
                    self.task.set_finish()

                else:
                    self.task.time = self.deck.time
                    self.task.set_break_time()

            self.task.break_time = self.deck.break_time
            self.change_status()
                
        elif self.task.is_break_time:
            for c in range(self.task.break_time):
                if not self.task.paused:
                    sleep(1)
                    self.break_time_decrease()
                    self.set_timer()
                    self.update()
                    
                else:
                    break
            
            self.task.set_running()
            self.change_status()