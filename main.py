from flet import *
from pages.homepage import *
from pages.createtask import *
def main(page: Page):
    page.fonts = {
        "Roboto": "/fonts/Roboto-Regular.ttf",
    }
    
    def mainContainer(e=None):
        return Container(
        width=414,
        height=455,
        border_radius=10,
        bgcolor='black' if cor == 'white' else 'white',
        content=Column(
            controls=[
                menuContainer(),
                selectContainer(),
                inputContainer(), 
                tasksContainer(),
                statusContainer()
            ]
        )
    )

    def createTaskContainer(e=None):
        return Container(
        width=414,
        height=455,
        border_radius=10,
        bgcolor='black' if cor == 'white' else 'white',
        content=Column(
            controls=[
                menuContainer(),
                deck_name_field(),
                task_time_field(),
                break_time_field(),
                repeat_time_field(),
                ring(page),
                footer(page)
            ]
        )
    )
    
    def route_change(e: RouteChangeEvent):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    mainContainer(),
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/createtask"))
                ]
            )
        )
        if page.route == "/createtask":
            page.views.append(
                View(
                    "/createtask",
                    [
                        createTaskContainer(),
                    ]
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