from flet import *
# from database.db import *
import os
import shutil

cor = "white"

def deck_name_field():
    global deck_name
    deck_name = TextField(
        label="Nome do Deck",
        width=272,
        height=50,
        color='white',
        border_color='blue',
        input_filter=InputFilter(allow=True, regex_string=r"[A-Za-z0-9 ]"),  # Permite letras, números e espaços
    )
    return Container(
        
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[deck_name]
        )
    )

def validate_deck_name():
    text = deck_name.value.strip()
    # Verifica se há pelo menos três caracteres não-espaciais
    if len([char for char in text if char.isalnum()]) >= 3:
        deck_name.error_text = None  # Remove o texto de erro se a validação for bem-sucedida
        return True
    else:
        deck_name.error_text = "O nome do deck deve conter pelo menos 3 caracteres não-espaciais."
        deck_name.update()
        return False
 
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
                Text(value="Tempo padrão de descanso em minutos", font_family="Roboto", color =cor),
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
                Text(value="Quantidade de repetições padrão", font_family="Roboto", color=cor),
                cicles
            ]
        )
    )

def ring(page):
    global selected_files
    def pick_files_result(e: FilePickerResultEvent):
        global path
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
        )

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text(value='alert-sound-loop-189741.mp3', font_family="Roboto", color='white', overflow='ELLIPSIS')

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
                    on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False, file_type=FilePickerFileType.AUDIO),
                )
            ]
        )
    )


def create_deck(page):
    if validate_deck_name():
        Database(deck_name.value)
        os.makedirs('assets/rings', exist_ok=True)

        if not os.path.exists(f'assets/rings/{selected_files.value}'):
            shutil.copy(path, f'assets/rings/{selected_files.value}')

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