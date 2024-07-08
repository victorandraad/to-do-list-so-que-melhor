from flet import *
from app.models.Database import Database

class WindowControls(WindowDragArea):
    def __init__(self, page) -> None:
        self.page = page
        self.cor = 'white'
        self.db: Database
        self.content = Row(
                alignment=MainAxisAlignment.END,
                controls=[
                    IconButton(icons.MINIMIZE, width=30, height=30, icon_size=15, icon_color=self.cor, on_click=self.minimize_window), 
                    # IconButton(icons.CLOSE_FULLSCREEN, width=30, height=30, icon_size=15, icon_color=cor),
                    IconButton(icons.CLOSE, width=30, height=30, icon_size=15, icon_color=self.cor, on_click=self.close_window)
                ]
        )
        super().__init__(content=self.content)
    
    def close_window(self, e):
        self.db.deck_name = 'deck temporário'
        self.db.delete_deck('deck temporário')
        self.update()
        self.page.window.close()
    
    def minimize_window(self, e):
        self.page.window.minimized = True
        self.page.update()