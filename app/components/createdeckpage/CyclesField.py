from flet import *

class CyclesField(Container):
    def __init__(self):
        super().__init__()

        self.cycles = CupertinoTextField(width=50, placeholder_text='3', text_align='center', value=3)

        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Quantidade de repetições padrão", font_family="Roboto", color='white'),
                self.cycles
            ]
        )