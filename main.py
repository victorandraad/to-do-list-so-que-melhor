from flet import *
from app.pages.createdeck import *
from app.models.Database import Database
from app.components.WindowControls import WindowControls
from app.components.DecksMenu import DecksMenu
from app.components.InputTask import InputTask
from app.components.TaskContainer import TaskContainer
from app.models.Deck import Deck

db = Database()

db.deck_name = 'deck temporário'

deck = Deck(
    'deck temporário',
    100,
    100,
    1,
    'app/assets/rings/alert-sound-loop-189741.mp3'
)

def main(page: Page):
    page.fonts = {
        "Roboto": "/fonts/Roboto-Regular.ttf",
    }
    
    page.title = "TOMODORO"
    page.window_bgcolor = colors.TRANSPARENT
    page.bgcolor = colors.TRANSPARENT
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_left = 400
    page.window_top = 200
    page.window_width = 425
    page.window_height = 450

    task_container = TaskContainer()
    task_container.db = db
    task_container.deck = deck

    decks_menu = DecksMenu(page, db)
    decks_menu.deck = deck
    decks_menu.task_container = task_container

    input_container = InputTask()
    input_container.db = db
    input_container.deck = deck
    input_container.task_container = task_container


    def mainContainer(e=None):
        return Container(
            border_radius= 10,
            bgcolor= 'black',
            content = Column(
                [
                    WindowControls(page),
                    decks_menu,
                    input_container, 
                    task_container,
                    # statusContainer(),
                ]
            )
        )
    # def createTaskContainer(e=None):
    #     return [
    #                 menuContainer(page),
    #                 deck_name_field(),
    #                 task_time_field(),
    #                 break_time_field(),
    #                 repeat_time_field(),
    #                 ring(page),
    #                 footer(page)
    #             ]
    
    def route_change(e: RouteChangeEvent):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    mainContainer(),
                ],
                bgcolor='transparent'
            )
        )

        # if page.route == "/createtask":
        #     page.views.append(
        #         View(
        #             "/createtask",
        #             createTaskContainer(),
        #             bgcolor='black'
        #         )
        #     )
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    task_container.update()


if __name__ == "__main__":
    app(target=main)
