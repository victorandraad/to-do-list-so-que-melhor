from flet import *
from app.models.Database import Database
from app.models.Deck import Deck
from app.models.Task import Item
from time import sleep
import pygame

cor = "white"
pygame.mixer.init()
    
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


def selectContainer(page, tasks_container):
    global subMenu
    # decks = Database().find_decks()
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

    def delete_deck(deck):
        Decks().delete(deck)
        page.go('/fdfasdf') # muda de página para uma ágina que não existe
        page.go('/')


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
    new_task = TextField(
        label="Escreva sua próxima tarefa",
        width=272,
        height=43, 
        color=cor,
        on_submit=lambda e: create_task(task_container, new_task))

    return Container(
        padding=padding.all(20),  # Add padding around the Row
        content=Row(
            alignment=MainAxisAlignment.START,
            controls=[
                new_task,
                IconButton(icons.CHECK, width=40, height=43, icon_color=cor, on_click=lambda _: create_task(task_container, new_task))
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
        if not db.search(n.value):
            db.insert(
                task = n.value,
                time = time,
                break_time = break_time,
                cicles = cicles,
            )
            updateTasksContainer(task_container, subMenu.content.value)
            n.error_text = None
        
        else:
            n.error_text = "Essa task já existe!"
        
        n.value = ""
        n.update()
        db.close()

def updateTasksContainer(tasks_container, deck_name = "deck temporário"):
    tasks = []
    ids = [icons.CHECK_BOX_OUTLINE_BLANK, icons.RADIO_BUTTON_CHECKED, icons.FREE_BREAKFAST, icons.PAUSE_ROUNDED, icons.CHECK_BOX]

    if deck_name:
        db = Database(deck_name)
        db_tasks = db.search_all()
        for n, c in enumerate(db_tasks):
            pygame.mixer.music.load(Decks().query(deck_name)[0]['ring'])
            icon_btn = IconButton(
                ids[c['id']],
                icon_color="#7094ff"
            )

            r2_controls = [
                        icon_btn,
                        Row(
                            controls=[Text(value=c['task'], font_family="Roboto", color=cor, width=200)],
                        ),
            ]

            r_controls = [
                Row(
                    controls=r2_controls
                ),
        
                IconButton(icons.DELETE, width=30, height=30, icon_size=15, icon_color='red', on_click=lambda e, task=c['task'], container=tasks_container:on_delete_task(task, container))
            ]

            row = Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=r_controls
                )

            def on_click_handler(e, icon_btn=icon_btn, r_controls=r_controls, row=row, db_task=c):
                define_task_status(icon_btn, r_controls, row, db_task)


            def on_delete_task(task, taskcontainer):
                db = Database(deck_name)
                db.delete(task)
                db.close()
                updateTasksContainer(taskcontainer, deck_name)
                
            icon_btn.on_click = on_click_handler

            tasks.insert(0, row)

    db.close()
    tasks_container.content.controls = tasks
    tasks_container.update()

def define_task_status(icon_btn, r_controls, row, db_task):
    db = Database(subMenu.content.value)
    def timer(r_controls, cicle, field):
        decks = Decks().query(subMenu.content.value)[0]

        match(field):
            case 'time':
                db.update({'break_time': decks['break_time']}, db_task['task'])
            
            case 'break_time':
                db.update({'time': decks['task_time']}, db_task['task'])

        new_db = db.search(db_task['task'])[0]

        sec = int(new_db[field][3:])
        minutes = int(new_db[field][:2])

        while True:
            if icon_btn.icon == icons.PAUSE_ROUNDED:
                break
            
            if sec == 0:
                sec = 59

                if minutes == 0:
                    task_manager(icon_btn, r_controls, cicle)
                    break
                
                else:
                    minutes -= 1

            else:
                sec -=1
            
            time = f"{minutes:02.0f}:{sec:02.0f}"
            db.update({field: time}, new_db['task'])
            new_total_time = (Decks().query(subMenu.content.value)[0]['total_time']) + 1
            Decks().update({'total_time': new_total_time}, subMenu.content.value)
            r_controls.insert(1, Text(value=time))
            row.update()
            sleep(1)
            r_controls.pop(1)


    def task_manager(icon_btn, r_controls, cicle):
        def stop_ring(e):
            pygame.mixer.music.stop()
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.play(-1)
        r_controls.append(AlertDialog(title=Text("Alarme"), on_dismiss=stop_ring, open=True, content=Text(value="Clique para parar o alarme.")))
        row.update()
        
        while pygame.mixer.music.get_busy():
            pass
        
        if icon_btn.icon == icons.FREE_BREAKFAST:
            icon_btn.icon = icons.RADIO_BUTTON_CHECKED
            db = Database(subMenu.content.value)
            db.update({'id': 1}, db_task['task'])
            timer(r_controls, cicle, 'time')

        elif icon_btn.icon == icons.RADIO_BUTTON_CHECKED:
            cicle += 1

            if cicle >= int(db_task['cicles']):
                icon_btn.icon = icons.CHECK_BOX
                db = Database(subMenu.content.value)
                db.update({'id': 4}, db_task['task'])
                r_controls.append(AlertDialog(title=Text("Tarefa concluida"), on_dismiss=stop_ring, open=True, content=Text(value="É hora de fazer outra coisa!")))
            
            else:
                icon_btn.icon = icons.FREE_BREAKFAST
                db = Database(subMenu.content.value)
                db.update({'id': 2}, db_task['task'])
                timer(r_controls, cicle, 'break_time')

    cicle = 0
    
    if icon_btn.icon == icons.CHECK_BOX_OUTLINE_BLANK:
        icon_btn.icon = icons.RADIO_BUTTON_CHECKED

        db.update({'id': 1}, db_task['task'])
        timer(r_controls, cicle, 'time')

    elif icon_btn.icon == icons.PAUSE_ROUNDED:
        if db.search(db_task['task'])[0]['id'] == 2:
            icon_btn.icon = icons.FREE_BREAKFAST
            db.update({'id': 2}, db_task['task'])
            timer(r_controls, cicle, 'break_time')
        
        elif db.search(db_task['task'])[0]['id'] == 1:
            icon_btn.icon = icons.RADIO_BUTTON_CHECKED
            db.update({'id': 1}, db_task['task'])
            timer(r_controls, cicle, 'time')

        

    elif icon_btn.icon == icons.CHECK_BOX:
        icon_btn.icon = icons.CHECK_BOX_OUTLINE_BLANK
        db.update({'id': 0}, db_task['task'])

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
    global status_container
    try:
        deck_info = Decks().query(subMenu.content.value)[0]
        spend_time = (deck_info['total_time'] / 60) / 60
    except:
        spend_time = 0

    status_container = Container(
        padding=padding.only(left=20, bottom=20),
        content=Row(
            controls=[
                Icon(icons.WATCH_LATER, size=50, color="#7094ff"),
                Text(value=f"{spend_time} horas estudadas", size=18, font_family="Roboto", color=cor),
            ]
        )
    )

    return status_container