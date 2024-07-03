from flet import *
from pages.homepage import *
from pages.createdeck import *

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

    def mainContainer(e=None):
        tasks_container = tasksContainer()
        return Container(
            border_radius= 10,
            bgcolor= 'black',
            content = Column(
                [
                    menuContainer(page),
                    selectContainer(page, tasks_container),
                    inputContainer(tasks_container), 
                    tasks_container,
                    # statusContainer(),
                ]
            )
        )
    def createTaskContainer(e=None):
        return [
                    menuContainer(page),
                    deck_name_field(),
                    task_time_field(),
                    break_time_field(),
                    repeat_time_field(),
                    ring(page),
                    footer(page)
                ]
    
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
        if page.route == "/createtask":
            page.views.append(
                View(
                    "/createtask",
                    createTaskContainer(),
                    bgcolor='black'
                )
            )
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    app(target=main)
