from flet import *

class DeckNameField(Container):
    def __init__(self):
        super().__init__()
        self.text_field = TextField(
            label="Nome do Deck",
            width=272,
            height=50,
            color='white',
            border_color='blue',
            input_filter=InputFilter(allow=True, regex_string=r"[A-Za-z0-9 ]"),
        )

        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.text_field
            ]
        )
    
    def validade_deck_name(self) -> bool:
        text = self.text_field.value.strip()
        # Verifica se há pelo menos três caracteres não-espaciais
        if len([char for char in text if char.isalnum()]) >= 3:
            self.text_field.error_text = None  # Remove o texto de erro se a validação for bem-sucedida
            return True
        else:
            self.text_field.error_text = "O nome do deck deve conter pelo menos 3 caracteres não-espaciais."
            self.text_field.update()
            return False