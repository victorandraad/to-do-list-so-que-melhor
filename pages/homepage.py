from flet import *

cor = "white"
    
def menuContainer():
    return Container(
        content=Row(
            alignment=MainAxisAlignment.END,
            controls=[
                IconButton(icons.MINIMIZE, width=30, height=30, icon_size=15, icon_color=cor), 
                IconButton(icons.CLOSE_FULLSCREEN, width=30, height=30, icon_size=15, icon_color=cor),
                IconButton(icons.CLOSE, width=30, height=30, icon_size=15, icon_color=cor)
            ]
        )
    )

def selectContainer():
    return Container(
        padding=padding.only(left=20),
        content=SearchBar(
            width=189,
            height=32,
            bar_bgcolor="#7094ff",
            bar_hint_text="Selecionar Deck",
            view_hint_text="Para criar um deck clique em \"+\"",
            view_elevation=4,
            view_bgcolor="#7094ff",
            divider_color=colors.BLACK,
            controls=[
                IconButton(icon=icons.CREATE_NEW_FOLDER, icon_color=colors.BLACK)
            ]
        )
    )
    
def inputContainer():
    return Container(
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                TextField(label="Escreva sua próxima tarefa", width=272, height=43, color=cor),
                IconButton(icons.EDIT, width=40, height=43, icon_color=cor),
                IconButton(icons.CHECK, width=40, height=43, icon_color=cor)
            ]
        )
    )
    
def tasksContainer():
    return Container(
        width=355,
        height=234,
        padding=padding.only(left=20),
        content=Column(
            scroll=ScrollMode.ADAPTIVE,
            controls=[
                Row(
                    controls=[
                        Icon(icons.CHECK_BOX, color="#7094ff"),
                        Text(value="Tarefa Finalizada", font_family="Roboto", color=cor) 
                    ]
                ),
                
                Row(
                    controls=[
                        Icon(icons.CHECK_BOX_OUTLINE_BLANK, color="#7094ff"),
                        Text(value="Tarefa para fazer", font_family="Roboto", color=cor)
                    ]
                ),
                
                Row(
                    controls=[
                        Icon(icons.RADIO_BUTTON_CHECKED, color="#7094ff"),
                        Text(value="Tarefa em curso", font_family="Roboto", color=cor)
                    ]
                ),
                
                Row(
                    controls=[
                        Icon(icons.PAUSE_ROUNDED, color="#7094ff"),
                        Text(value="Tarefa pausada pelo usuário", font_family="Roboto", color=cor)
                    ]
                ),
                
                Row(
                    controls=[
                       Icon(icons.FREE_BREAKFAST, color="#7094ff"),
                        Text(value="Break time", font_family="Roboto", color=cor) 
                    ]
                ),
            ]
        )
    )
    
def statusContainer():
    return Container(
        padding=padding.only(left=20),
        content=Row(
            controls=[
                Icon(icons.WATCH_LATER, size=50, color="#7094ff"),
                Text(value="215 horas estudadas", size=18, font_family="Roboto", color=cor),
            ]
        )
    )