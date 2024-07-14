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
        self.width= 400
        self.height=234
        self.padding=padding.only(left=20)
        self.dialog_change_deck: AlertDialog = None
        self.dialog_create_deck: AlertDialog = None

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

        self.db: Database
        self.deck: Deck

    def update(self, force=False):
        if not self.get_active_task(None) or force:
            self.queue_tasks.clear()
            self.tasks.clear()

            if self.dialog_change_deck != None:
                self.queue_tasks.append(self.dialog_change_deck)
                self.queue_tasks.append(self.dialog_create_deck)
            
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
        return TaskRow(self.db, task, self.deck, self.get_active_task, self.update)

    def get_active_task(self, task_name) -> bool:
        """
        False = no active tasks
        else: return task
        """
        for task in self.tasks:
            if task.controls[0].controls[0].icon not in (icons.CHECK_BOX_OUTLINE_BLANK, icons.CHECK_BOX):
                if task_name != task.controls[0].controls[1].controls[0].value:
                    return True

        return False

class TaskRow(Row):
    def __init__(self, db: Database, task: Task, deck: Deck, get_active_task, container_update) -> None:
        super().__init__()

        self.task: Task = task
        self.db: Database = db
        self.deck: Deck = deck
        self.get_active_task = get_active_task
        self.container_update = container_update

        self.alarm = Audio(
            src=self.task.sound,
            volume=1,
        )

        self.status = [
            icons.CHECK_BOX_OUTLINE_BLANK, # nao feito  - 0 
            icons.RADIO_BUTTON_CHECKED, # fazendo  - 1 
            icons.FREE_BREAKFAST, # break  - 2 
            icons.PAUSE_ROUNDED, # pause  - 3 
            icons.CHECK_BOX # finished  - 4 
        ]

        self.dialog_start_another_task_error = AlertDialog(
            bgcolor='black',
            modal=True,
            title=Text("Atenção!", color=colors.BLUE), 
            open=False,
            content=Text(value="Você deve terminar uma tarefa antes de começar outra."), 
            actions=[TextButton("Voltar.", on_click=self.decline_change),]
        )

        self.running_task_alarm = AlertDialog(
            bgcolor='black',
            modal=True, 
            title=Text("Vamos voltar com toda concentração!", color=colors.BLUE),
            content=Text(value="Valorize o tempo de descanso para voltar muito mais firme 😎"), 
            open=False,
            actions=[TextButton("Vamos!", on_click=self.decline_change, ),]
        )

        self.break_time_task_alarm = AlertDialog(
            bgcolor='black',
            modal=True, 
            title=Text("Hora de descansar.", color=colors.BLUE), 
            open=False,
            content=Text(value="Nesse tempo não ouse pensar sobre isso!"), 
            actions=[TextButton("Ir ao descanso.", on_click=self.decline_change, ),]
        )

        self.finish_task_alarm = AlertDialog(
            bgcolor='black',
            modal=True, 
            title=Text("Parabéns!", color=colors.GREEN), 
            open=False,
            content=Text(value="Por agora já deu disso, mas caso ainda não tenha terminado você pode começar outro ciclo.🫡 \nO tempo recomendado para voltar a fazer a mesma atividade é depois de pelo menos 1 hora."), 
            actions=[TextButton("Voltar.", on_click=self.decline_change, ),]
        )

        self.icon_status = IconButton(
            icon=self.status[self.task.status],
            icon_color="#7094ff",
            on_click=self.change_status_click
        )

        self.edit_task_form = AlertDialog(
            bgcolor=colors.BLUE,
            modal=True,
            open=False,
            title=Text(f"Edit task '{self.task.name}'", color=colors.WHITE),

            content=Column(
                width=300,
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    name:=TextField(
                        border_color=colors.WHITE,
                        label_style=TextStyle(color=colors.WHITE),
                        label="Nome da tarefa.",
                        value=f"{self.task.name}",
                        width=272,
                        height=43, 
                        color='white',
                    ),

                    time:= TextField(
                        border_color=colors.WHITE,
                        label_style=TextStyle(color=colors.WHITE),
                        label="Tempo da tarefa.",
                        value=f"{int(self.task.time / 60)}",
                        width=272,
                        height=43, 
                        color='white',
                    ),

                    break_time:= TextField(
                        border_color=colors.WHITE,
                        label_style=TextStyle(color=colors.WHITE),
                        label="Tempo de descanso da tarefa.",
                        value=f"{int(self.task.break_time / 60)}",
                        width=272,
                        height=43, 
                        color='white',
                    ),

                    cycles:= TextField(
                        border_color=colors.WHITE,
                        label_style=TextStyle(color=colors.WHITE),
                        label="Quantidade de ciclos da tarefa.",
                        value=f"{int(self.task.cycles)}",
                        width=272,
                        height=43, 
                        color='white',
                    )
                ]
            ),

            actions=[
                TextButton("Voltar.", on_click=self.decline_change, style=ButtonStyle(color=colors.WHITE)),
                TextButton(
                    "Editar Task.", 
                    on_click=lambda _: self.edit_task(name.value, time.value, break_time.value, cycles.value), 
                    style=ButtonStyle(color=colors.WHITE) 
                ),
            ],
        )

        self.task_options = BottomSheet(
            bgcolor=colors.BLUE,
            content=Row(
                controls=[
                    TextButton(
                        text="Editar",
                        icon=icons.EDIT,
                        style=ButtonStyle(color=colors.WHITE),
                        on_click=self.show_edit_task_form     
                    ),
                    TextButton(
                        text="Finalizar",
                        icon=icons.VERIFIED,
                        icon_color=colors.GREEN,
                        on_click=self.finalize_from_btn,
                        style=ButtonStyle(color=colors.WHITE),
                    ),
                    TextButton(
                        text="Excluir",
                        icon=icons.DELETE,
                        icon_color=colors.RED,
                        on_click=self.delete_task,
                        style=ButtonStyle(color=colors.WHITE),
                    )
                ],
                tight=True,
            ),
        
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
            IconButton(icons.MORE_VERT, width=30, height=30, icon_size=15, on_click=self.show_task_options),

            self.task_options,
            self.dialog_start_another_task_error,
            self.finish_task_alarm,
            self.break_time_task_alarm,
            self.running_task_alarm,
            self.alarm,
            self.edit_task_form,
        ]

    def edit_task(self, name, time, break_time, cycles):
        self.task.time = int(time) * 60
        self.task.break_time = int(break_time) * 60
        self.task.cycles = int(cycles)

        self.db.edit_task(self.task, name=name, time=self.task.time, break_time=self.task.break_time, cycles=self.task.cycles)

        self.task.name = name

        self.controls[0].controls[1].controls[0].value = self.task.name

        self.decline_change(e=None)

    def show_edit_task_form(self, e):
        self.edit_task_form.open = True
        self.update()

    def finalize_from_btn(self, e):
        self.task.set_finish() 
        self.db.edit_task(self.task, status=4)
        self.hide_task_options()
        self.task.time = self.deck.time
        self.task.break_time = self.deck.break_time
        self.task.cycles = self.deck.cycles
        self.change_status()

    def show_task_options(self, e):
        self.task_options.open = True

        if self.task.status != 0 and not self.task.status == 4:
            self.task_options.content.controls[0].visible = False
        else:
            self.task_options.content.controls[0].visible = True

        self.update()
    
    def hide_task_options(self):
        self.task_options.open = False
        self.page.update() 

    def decline_change(self, e):
        self.edit_task_form.open = False
        self.task_options.open = False
        self.dialog_start_another_task_error.open = False
        self.finish_task_alarm.open = False
        self.break_time_task_alarm.open = False
        self.running_task_alarm.open = False
        self.alarm.pause()
        self.change_status()
        self.update()

    def delete_task(self, e):
        self.hide_task_options()
        self.db.delete_task(self.task)
        self.visible = False
        self.task.set_blank()
        self.icon_status.icon = self.status[0]
        self.update()

    def change_status(self):
        self.icon_status.icon = self.status[self.task.status]
        self.icon_status.update()

        if self.icon_status.icon == self.status[4]:
            self.container_update()
        else:   
            self.set_timer()
            self.update()
            self.timer()
        
        self.update()   


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
    
    def running_alarm(self):
        self.running_task_alarm.open = True
        self.alarm.play()
    
    def break_time_alarm(self):
        self.break_time_task_alarm.open = True
        self.alarm.play()
    
    def finish_alarm(self):
        self.finish_task_alarm.open = True
        self.alarm.play()

    def timer(self):
        if self.task.running:
            for c in range(self.task.time):
                if not self.task.paused and self.task.running:
                    sleep(1)
                    self.time_decrease()
                    self.set_timer()
                    self.update()

                else:
                    break

        if self.task.running:
            if self.task.time <= 0:
                self.task.cycles -= 1

                if self.task.cycles <= 0:
                    self.task.time = self.deck.time
                    self.task.cycles = self.deck.cycles
                    self.task.set_finish()
                    self.db.edit_task(self.task, status=4)
                    self.finish_alarm()

                else:
                    self.task.time = self.deck.time
                    self.task.set_break_time()
                    self.break_time_alarm()

            self.task.break_time = self.deck.break_time
            self.update()
                
        elif self.task.is_break_time:
            for _ in range(self.task.break_time + 1):
                if self.task.is_break_time:
                    if self.task.break_time <= 0:
                        self.task.set_running()
                        self.running_alarm()
                    
                    elif not self.task.paused:
                        sleep(1)
                        self.break_time_decrease()
                        self.set_timer()
                     
                else: break
                
                self.update()

            