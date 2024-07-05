from flet import *
from app.models.Database import Database
from app.models.Deck import Deck
from app.models.Task import Task
from time import sleep
import pygame


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