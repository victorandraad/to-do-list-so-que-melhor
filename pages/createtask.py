from flet import *
from database.db import *

cor = "white"

def deck_name_field():
    global deck_name
    deck_name = TextField(label="Nome do Deck", width=272, height=43, color=cor, border_color='blue')
    return Container(
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                deck_name
            ]
        )
    )
 
def task_time_field():
    global task_time
    task_time = CupertinoTextField(width=50, placeholder_text='25', text_align='center', value=25)
    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Tempo padrão de tasks em minutos", font_family="Roboto", color =cor),
                task_time
            ]
        )
    )

def break_time_field():
    global break_time
    break_time = CupertinoTextField(width=50, placeholder_text='5', text_align='center', value=5)
    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Tempo padrão de tasks em minutos", font_family="Roboto", color =cor),
                break_time
            ]
        )
    )

def repeat_time_field():
    global cicles
    cicles = CupertinoTextField(width=50, placeholder_text='3', text_align='center', value=3)
    return Container(
        padding=10,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(value="Quantidade de repetições padrão", font_family="Roboto", color =cor),
                cicles
            ]
        )
    )

def ring(page):
    global selected_files
    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text(value='alert-sound-loop-189741.mp3', font_family="Roboto", color =cor, overflow='ELLIPSIS')

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

def create_deck(page):
    Database(deck_name.value)
    Decks().configs(deck_name.value, task_time.value, break_time.value, cicles.value, selected_files.value)
    page.go("/")

def footer(page):
    return Container(
        padding=20,
        content=Row(
            alignment=MainAxisAlignment.END,
            vertical_alignment=VerticalAlignment.END,
            controls=[
                ElevatedButton("Cancelar", on_click= lambda _: page.go("/")),
                ElevatedButton("Criar", on_click= lambda _: create_deck(page))
            ]
        )
    )