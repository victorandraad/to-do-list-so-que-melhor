from flet import *


class TaskTimeField(Container):
    def __init__(self):
        super().__init__()
        self.task_time = CupertinoTextField(width=50, placeholder_text='25', text_align='center', value=25)

        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Tempo padrão de tasks em minutos", font_family="Roboto", color='white'),
                self.task_time
            ]
        )
        