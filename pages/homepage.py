from flet import *
from database.db import *
from time import sleep

cor = "white"
    
def menuContainer(page):
    def close_window():
        if os.path.exists('database/decks/deck temporário.json'):
            Decks().delete("deck temporário")
        page.window_destroy()
        
    return Container(
        content=Row(
            alignment=MainAxisAlignment.END,
            controls=[
                IconButton(icons.MINIMIZE, width=30, height=30, icon_size=15, icon_color=cor), 
                IconButton(icons.CLOSE_FULLSCREEN, width=30, height=30, icon_size=15, icon_color=cor),
                IconButton(icons.CLOSE, width=30, height=30, icon_size=15, icon_color=cor, on_click=lambda _: close_window())
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
            deck = False
            time = 25
            break_time = 5
            cicles = 3

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
            'cicles': cicles
        })
        updateTasksContainer(task_container, subMenu.content.value)

def updateTasksContainer(tasks_container, deck_name):
    tasks = []
    ids = [icons.CHECK_BOX_OUTLINE_BLANK, icons.RADIO_BUTTON_CHECKED, icons.FREE_BREAKFAST, icons.PAUSE_ROUNDED, icons.CHECK_BOX]

    if deck_name:
        db = Database(deck_name)
        db_tasks = db.search_all()
        for c in db_tasks:
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
    def timer(r_controls):
        sec = int(r_controls[1].value[3:])
        minutes = int(r_controls[1].value[:2])
        while True:
            if icon_btn.icon == icons.PAUSE_ROUNDED:
                break
            
            if sec == 0:
                sec = 59
                minutes -= 1
            else:
                sec -=1
            
            r_controls.pop(1)
            r_controls.insert(1, Text(value=f"{minutes}:{sec:02.0f}"))
            row.update()
            sleep(1)

            if minutes == 0:
                break


    if icon_btn.icon == icons.CHECK_BOX_OUTLINE_BLANK:
        icon_btn.icon = icons.RADIO_BUTTON_CHECKED
        r_controls.insert(1, Text(value=f'{db_task["time"]}:00'))
        timer(r_controls)

    elif icon_btn.icon == icons.PAUSE_ROUNDED:
        icon_btn.icon = icons.RADIO_BUTTON_CHECKED
        timer(r_controls)

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