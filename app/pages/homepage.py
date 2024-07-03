from flet import *
from app.models.Database import Database
from app.models.Deck import Deck
from app.models.Task import Task
from time import sleep
import pygame

cor = "white"
pygame.mixer.init()

DB = Database('deck temporário')

DECK = Deck(
    name        ='deck temporário',
    time        = 5,
    break_time  = 5,
    cycles      = 3,
    sound       = r'app\assets\rings\alert-sound-loop-189741.mp3'
)

TASK = Task(
    name        ='deck temporário',
    time        = 5,
    break_time  = 5,
    cycles      = 3,
    sound       = r'app\assets\rings\alert-sound-loop-189741.mp3',
    status      = 0
)

status = [icons.CHECK_BOX_OUTLINE_BLANK, icons.RADIO_BUTTON_CHECKED, icons.FREE_BREAKFAST, icons.PAUSE_ROUNDED, icons.CHECK_BOX]

tasks = []

tasksContainer = Container(
        width=355,
        height=234,
        padding=padding.only(left=20),
        content=Column(
            scroll=ScrollMode.ADAPTIVE,
            controls=tasks
        )
    )


    
def menuContainer(page):
    def close_window(e):
        page.window_close()
    
    def minimize_window(e):
        page.window_minimized = True
        page.update()
        
    return WindowDragArea(
        Row(
            alignment=MainAxisAlignment.END,
            controls=[
                IconButton(icons.MINIMIZE, width=30, height=30, icon_size=15, icon_color=cor, on_click=minimize_window), 
                # IconButton(icons.CLOSE_FULLSCREEN, width=30, height=30, icon_size=15, icon_color=cor),
                IconButton(icons.CLOSE, width=30, height=30, icon_size=15, icon_color=cor, on_click=close_window)
            ]
        )
    )


def selectContainer(page):
    global subMenu
    deckname = "deck temporário"
    menuItems = []

    def updateDeck(deck_name):
        subMenu.content = Text(deck_name, color=cor, size=20)

        DB.name = deck_name
        DECK.name = DB.name

        DB.create_deck(DECK)

        DECK.name,
        DECK.time,
        DECK.break_time,
        DECK.sound,
        DECK.cycles = DB.find_deck()

        subMenu.update()

    def delete_deck(deck):
        DECK.name = deck
        DB.delete_deck(DECK)

        update_menu_items()
        subMenu.update()

    def update_menu_items():
        menuItems.clear()
        decks = DB.find_decks()
        for deck in decks:
            menuItems.append(
                Container(
                    padding=padding.all(10),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        
                        controls=[
                            MenuItemButton(
                                content=Text(deck),
                                leading=Icon(icons.FOLDER),
                                style=ButtonStyle(bgcolor={MaterialState.HOVERED: colors.GREEN}),
                                on_click=lambda e, deck=deck: updateDeck(deck),
                            ),

                            IconButton(icons.DELETE, width=30, height=30, icon_size=15, icon_color='red', on_click=lambda e, deck=deck: delete_deck(deck)), 
                        ]
                    )
                )
                
            )

        menuItems.append(
            MenuItemButton(
                content=Text("Criar novo deck."),
                leading=Icon(icons.CREATE_NEW_FOLDER),
                style=ButtonStyle(bgcolor={MaterialState.HOVERED: colors.BLUE}),
                on_click=lambda _: page.go("/createtask")
            )
        )

    update_menu_items()

    subMenu = SubmenuButton(
        content=Text(deckname, color=cor, size=20),
        controls=menuItems
    )

    return Container(
        padding=padding.only(left=20, bottom=10, right=20),
        content=MenuBar(
            expand=True,
            style=MenuStyle(
                alignment=alignment.center,
                bgcolor=colors.BLUE,
                mouse_cursor={
                    MaterialState.HOVERED: MouseCursor.WAIT,
                    MaterialState.DEFAULT: MouseCursor.ZOOM_OUT
                },
            ),
            controls=[subMenu]
        )
    )


def inputContainer():
    new_task = TextField(
        label="Escreva sua próxima tarefa",
        width=272,
        height=43, 
        color=cor,
        on_submit=lambda e: create_task(new_task.value))

    def create_task(name):
        DB.create_task(
            Task(
                name        = name,
                time        = DECK.time,
                status      = 0,
                break_time  = DECK.break_time,
                cycles      = DECK.cycles,
                sound       = DECK.sound
            )
        )

        DECK.tasks = DB.find_tasks()
        updateTasksContainer()
        tasksContainer.update()

    return Container(
        padding=padding.all(20),  # Add padding around the Row
        content=Row(
            alignment=MainAxisAlignment.START,
            controls=[
                new_task,
                IconButton(icons.CHECK, width=40, height=43, icon_color=cor, on_click=lambda _: create_task(new_task.value))
            ]
        )
    )


def updateTasksContainer():
    tasks.clear()
    DECK.tasks = DB.find_tasks()
    for c in DECK.tasks:
        this_task = Task(
            name = c['name'],
            status = c['status'],
            sound = c['sound'],
            time = c['time'],
            break_time = c['break_time'],
            cycles = c['cycles'],
        )

        

        pygame.mixer.music.load(this_task.sound)

        icon_btn = IconButton(
            status[this_task.status],
            icon_color="#7094ff",
        )

        r2_controls = [
            icon_btn,
            Row(
                controls=[Text(value=this_task.name, font_family="Roboto", color=cor, width=200)],
            ),
        ]

        r_controls = [
            Row(
                controls=r2_controls
            ),
    
            IconButton(icons.DELETE, width=30, height=30, icon_size=15, icon_color='red', on_click=lambda e, this_task=this_task:on_delete_task(this_task))
        ]

        row = Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=r_controls
            )

        def on_click_handler(e, icon_btn=icon_btn, r_controls=r_controls, row=row, task=this_task):
            define_task_status(icon_btn, r_controls, row, task)


        def on_delete_task(task):
            DB.delete_task(task)
            updateTasksContainer()
            tasksContainer.update()
            
        icon_btn.on_click = on_click_handler

        tasks.insert(0, row)


def define_task_status(icon_btn, r_controls, row, this_task):
    def timer():
        if this_task.is_break_time:
            time = this_task.break_time

        elif this_task.running:
            time = this_task.time
            this_task.cycles -= 1
            DB.edit_task(this_task, cycles = this_task.cycles)

        while True:
            if icon_btn.icon == icons.PAUSE_ROUNDED:
                break
            
            elif time > 0:
                time -= 1
            
            elif time == 0:
                task_manager()
                break
            
            minutes, seconds = divmod(time, 60)

            if this_task.is_break_time:
                DB.edit_task(this_task, break_time = time)

            elif this_task.running:
                DB.edit_task(this_task, time = time)
            
            # new_total_time = (Decks().query(subMenu.content.value)[0]['total_time']) + 1
            # Decks().update({'total_time': new_total_time}, subMenu.content.value)
            r_controls.insert(1, Text(value=f'{minutes:02.0f}:{seconds:02.0f}'))
            row.update()
            r_controls.pop(1)
            sleep(1)

    def task_manager():
        def stop_ring(e):
            pygame.mixer.music.stop()
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.play(-1)
        r_controls.append(AlertDialog(title=Text("Alarme"), on_dismiss=stop_ring, open=True, content=Text(value="Clique para parar o alarme.")))
        row.update()
        
        while pygame.mixer.music.get_busy():
            pass

        if this_task.cycles <= 0:
            this_task.set_finish()
            r_controls.append(AlertDialog(title=Text("Tarefa concluida"), on_dismiss=stop_ring, open=True, content=Text(value="É hora de fazer outra coisa!")))
            DB.edit_task(this_task, cycles = DECK.cycles)

        elif this_task.running:
            this_task.set_break_time()

        elif this_task.is_break_time:
            this_task.set_running()

        DB.edit_task(this_task, time = DECK.time, break_time = DECK.break_time)
        icon_btn.icon = status[this_task.status]

        if not this_task.finish:
            timer()

        
        

    this_task.click()
    icon_btn.icon = status[this_task.status]
    
    DB.edit_task(this_task, status = this_task.status)

    if not this_task.previous_status == 4:
        timer()

    row.update()
    icon_btn.update()

    


def statusContainer():
    status_container = Container(
        padding=padding.only(left=20, bottom=20),
        content=Row(
            controls=[
                Icon(icons.WATCH_LATER, size=50, color="#7094ff"),
                Text(value=f"Tantas horas estudadas", size=18, font_family="Roboto", color=cor),
            ]
        )
    )

    return status_container