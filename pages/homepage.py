from flet import *
from database.db import *

cor = "white"
    
def menuContainer(page):
    def close_window():
        if os.path.exists('database/deck temporário.json'):
            Decks().delete("deck temporário")
        page.window_close()
        
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
                bgcolor="#7094ff",
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

    def create_task(n):
        db = Database(subMenu.content.value)
        db.insert({
            'task': n,
            'id': 0
        })
        updateTasksContainer(task_container, subMenu.content.value)
    return Container(
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                new_task,
                IconButton(icons.EDIT, width=40, height=43, icon_color=cor, on_click=lambda _: print('clicou aqui')),
                IconButton(icons.CHECK, width=40, height=43, icon_color=cor, on_click=lambda _: create_task(new_task.value))
            ]
        )
    )

def updateTasksContainer(tasks_container, deck_name):
    tasks = []
    ids = [icons.CHECK_BOX_OUTLINE_BLANK, icons.RADIO_BUTTON_CHECKED, icons.FREE_BREAKFAST, icons.PAUSE_ROUNDED, icons.CHECK_BOX]

    if deck_name:
        db = Database(deck_name)
        db_tasks = db.search_all()
        for c in db_tasks:
            tasks.append(
                Row(
                    controls=[
                        IconButton(ids[c['id']], icon_color="#7094ff"),
                        Text(value=c['task'], font_family="Roboto", color=cor)
                    ]
                )
            )

    tasks_container.content.controls = tasks
    tasks_container.update()

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