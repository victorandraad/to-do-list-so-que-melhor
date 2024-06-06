from flet import *

cor = "white"

def deck_name_field():
    return Container(
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                TextField(label="Nome do Deck", width=272, height=43, color=cor, border_color='blue')
            ]
        )
    )
 
def task_time_field():
    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Tempo padrão de tasks em minutos", font_family="Roboto", color =cor),
                CupertinoTextField(width=50, placeholder_text='25', text_align='center')
            ]
        )
    )

def break_time_field():
    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Tempo padrão de tasks em minutos", font_family="Roboto", color =cor),
                CupertinoTextField(width=50, placeholder_text='5', text_align='center')
            ]
        )
    )

def repeat_time_field():
    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Quantidade de repetições padrão", font_family="Roboto", color =cor),
                CupertinoTextField(width=50, placeholder_text='3', text_align='center')
            ]
        )
    )

def ring(page):

    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text(value="Som de alarme padrão", font_family="Roboto", color =cor, overflow='ELLIPSIS')

    page.overlay.append(pick_files_dialog)

    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                selected_files,
                ElevatedButton(
                    "Selecionar Arquivo",
                    icon=icons.UPLOAD,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                )
            ]
        )
    )

def footer(page):
    return Container(
        padding=20,
        content=Row(
            alignment=MainAxisAlignment.END,
            vertical_alignment=VerticalAlignment.END,
            controls=[
                ElevatedButton("Cancelar", on_click= lambda _: page.go("/")),ElevatedButton("Criar", on_click= lambda _: page.go("/"))
            ]
        )
    )