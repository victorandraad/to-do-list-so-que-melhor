from flet import *

class WindowControls(WindowDragArea):
    def __init__(self, page) -> None:
        super().__init__()
        self.page = page
        self.cor = 'white'
        self.content = Row(
                alignment=MainAxisAlignment.END,
                controls=[
                    IconButton(icons.MINIMIZE, width=30, height=30, icon_size=15, icon_color=self.cor, on_click=self.minimize_window), 
                    # IconButton(icons.CLOSE_FULLSCREEN, width=30, height=30, icon_size=15, icon_color=cor),
                    IconButton(icons.CLOSE, width=30, height=30, icon_size=15, icon_color=self.cor, on_click=self.close_window)
                ]
            )
    
    def close_window(self, e):
        self.page.window_close()
    
    def minimize_window(self, e):
        self.page.window_minimized = True
        self.page.update()