from flet import *

class RingField(Container):
    def __init__(self):
        super().__init__()

        self.selected_files = Text(value='alert-sound-loop-189741.mp3', font_family="Roboto", color='white', overflow='ELLIPSIS')

        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)

        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.selected_files,
                ElevatedButton(
                    "Selecionar Arquivo",
                    icon=icons.UPLOAD,
                    on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False, file_type=FilePickerFileType.AUDIO),
                )
            ]
        )
    
    def pick_files_result(self, e: FilePickerResultEvent):
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.selected_files.update()
        self.path = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "")