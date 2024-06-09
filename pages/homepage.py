from flet import *
from database.db import *
from time import sleep
import pygame

cor = "white"
pygame.mixer.init()
    
def menuContainer(page):
    def close_window(e):
        if os.path.exists('database/decks/deck temporário.json'):
            Decks().delete("deck temporário")
        page.window_destroy()
    
    def minimize_window(e):
        page.window_minimized = True
        page.update()
        
    return Container(
        content=Row(
            alignment=MainAxisAlignment.END,
            controls=[
                IconButton(icons.MINIMIZE, width=30, height=30, icon_size=15, icon_color=cor, on_click=minimize_window), 
                # IconButton(icons.CLOSE_FULLSCREEN, width=30, height=30, icon_size=15, icon_color=cor),
                IconButton(icons.CLOSE, width=30, height=30, icon_size=15, icon_color=cor, on_click=close_window)
            ]
        )
    )

def selectContainer(page, tasks_container):
    global subMenu
    decks = Decks().list_decks()
    deckname = "deck temporário"

    menuItems = []

    subMenu = SubmenuButton(
        content=Text(deckname, color=cor, size=20),
        controls=menuItems
    )

    def updateDeck(deck_name):
        subMenu.content = Text(deck_name, color=cor, size=20)
        updateTasksContainer(tasks_container, deck_name)
        page.update()


    for deck in decks:
        menuItems.append(
            MenuItemButton(
                content=Text(deck),
                leading=Icon(icons.FOLDER),
                style=ButtonStyle(bgcolor={MaterialState.HOVERED: colors.GREEN}),
                on_click=lambda e, deck=deck: updateDeck(deck)
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

def inputContainer(task_container):
    new_task = TextField(label="Escreva sua próxima tarefa", width=272, height=43, color=cor)

    return Container(
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                new_task,
                IconButton(icons.EDIT, width=40, height=43, icon_color=cor, on_click=lambda _: print('clicou aqui')),
                IconButton(icons.CHECK, width=40, height=43, icon_color=cor, on_click=lambda _: create_task(task_container, new_task.value))
            ]
        )
    )

def create_task(task_container, n, time=False, break_time=False, cicles=False):
        try:
            deck = Decks().query(subMenu.content.value)[0]
        except:
            Decks().configs(subMenu.content.value)
            deck = Decks().query(subMenu.content.value)[0]

        if deck:
            if not time:
                time = deck['task_time']

            if not break_time:
                break_time = deck['break_time']

            if not cicles:
                cicles = deck['cicles']
    
        db = Database(subMenu.content.value)
        db.insert({
            'task': n,
            'id': 0,
            'time': time,
            'break_time': break_time,
            'cicles': cicles,
            'ring' : "assets/rings/alert-sound-loop-189741.mp3"
        })
        updateTasksContainer(task_container, subMenu.content.value)

def updateTasksContainer(tasks_container, deck_name):
    tasks = []
    ids = [icons.CHECK_BOX_OUTLINE_BLANK, icons.RADIO_BUTTON_CHECKED, icons.FREE_BREAKFAST, icons.PAUSE_ROUNDED, icons.CHECK_BOX]

    if deck_name:
        db = Database(deck_name)
        db_tasks = db.search_all()
        for c in db_tasks:
            pygame.mixer.music.load(Decks().query(deck_name)[0]['ring'])
            icon_btn = IconButton(
                ids[c['id']],
                icon_color="#7094ff"
            )

            r_controls = [
                icon_btn,
                Text(value=c['task'], font_family="Roboto", color=cor)
            ]

            row = Row(
                    controls=r_controls
                )

            def on_click_handler(e, icon_btn=icon_btn, r_controls=r_controls, row=row, db_task=c):
                define_task_status(icon_btn, r_controls, row, db_task)
                
            icon_btn.on_click = on_click_handler

            tasks.insert(0, row)

    tasks_container.content.controls = tasks
    tasks_container.update()

def define_task_status(icon_btn, r_controls, row, db_task):
    def timer(r_controls, cicle):
        sec = int(r_controls[1].value[3:])
        minutes = int(r_controls[1].value[:2])
        while True:
            if icon_btn.icon == icons.PAUSE_ROUNDED:
                break
            
            if sec == 0:
                sec = 59

                if minutes == 0:
                    task_manager(r_controls, cicle)
                    break
                
                else:
                    minutes -= 1

            else:
                sec -=1
            
            r_controls.pop(1)
            r_controls.insert(1, Text(value=f"{minutes:02.0f}:{sec:02.0f}"))
            row.update()
            sleep(1)


    def task_manager(r_controls, cicle):
        def stop_ring(e):
            pygame.mixer.music.stop()
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.play(-1)
        r_controls.append(AlertDialog(title=Text("Alarme"), on_dismiss=stop_ring, open=True, content=Text(value="Clique para parar o alarme.")))
        row.update()

        while pygame.mixer.music.get_busy():
            pass

        if r_controls[0].icon == icons.FREE_BREAKFAST:
            r_controls[0].icon = icons.RADIO_BUTTON_CHECKED
            r_controls.pop(1)
            r_controls.insert(1, Text(value=f"{int(db_task['time']):02.0f}:00"))
            timer(r_controls, cicle)

        elif r_controls[0].icon == icons.RADIO_BUTTON_CHECKED:
            cicle += 1

            if cicle >= int(db_task['cicles']):
                r_controls[0].icon = icons.CHECK_BOX
                r_controls.pop(1)
                db = Database(subMenu.content.value)
                db.update({
                    'id': 4
                }, db_task['task'])
                r_controls.append(AlertDialog(title=Text("Tarefa concluida"), on_dismiss=stop_ring, open=True, content=Text(value="É hora de fazer outra coisa!")))
            
            else:
                r_controls[0].icon = icons.FREE_BREAKFAST
                r_controls.pop(1)
                r_controls.insert(1, Text(value=f"{int(db_task['break_time']):02.0f}:00"))
                timer(r_controls, cicle)

    cicle = 0
    
    if icon_btn.icon == icons.CHECK_BOX_OUTLINE_BLANK:
        icon_btn.icon = icons.RADIO_BUTTON_CHECKED
        # r_controls.insert(1, Text(value=f'00:03'))
        r_controls.insert(1, Text(value=f'{int(db_task["time"]):02.0f}:00'))
        timer(r_controls, cicle)

    elif icon_btn.icon == icons.PAUSE_ROUNDED:
        icon_btn.icon = icons.RADIO_BUTTON_CHECKED
        timer(r_controls, cicle)

    elif icon_btn.icon == icons.CHECK_BOX:
        icon_btn.icon = icons.CHECK_BOX_OUTLINE_BLANK
        db = Database(subMenu.content.value)
        db.update(
            {
                'id': 0
            }, db_task['task']
        )

    else:
        icon_btn.icon = icons.PAUSE_ROUNDED

    row.update()
    icon_btn.update()

def tasksContainer():
    return Container(
        width=355,
        height=234,
        padding=padding.only(left=20),
        content=Column(
            scroll=ScrollMode.ADAPTIVE,
            controls=[]
        )
    )


def statusContainer():
    return Container(
        padding=padding.only(left=20),
        content=Row(
            controls=[
                Icon(icons.WATCH_LATER, size=50, color="#7094ff"),
                Text(value="215 horas estudadas", size=18, font_family="Roboto", color=cor),
            ]
        )
    )