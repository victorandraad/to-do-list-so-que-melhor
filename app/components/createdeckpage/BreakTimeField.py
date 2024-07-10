from flet import * 

class BreakTimeField(Container):
    def __init__(self):
        super().__init__()

        self.break_time = CupertinoTextField(width=50, placeholder_text='5', text_align='center', value=5)

        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Tempo padrão de descanso em minutos", font_family="Roboto", color='white'),
                self.break_time
            ]
        )