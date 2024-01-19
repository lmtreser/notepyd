# Editor de textos simple
# Lucas Martín Treser - Agosto de 2023

from guizero import App, Box, MenuBar, PushButton, Text, TextBox, Window, yesno
from tkinter import Menu
from datetime import datetime

#-- Funciones menu ARCHIVO
def file_open():
    estado.value = "Abrir archivo "
    ruta = notepad.select_file(title="Abrir archivo", folder=".", filetypes=[["Texto", ".txt"]])
    archivo = open(str(ruta), "r")
    texto.value = archivo.read()
    archivo.close()

def file_save():
    estado.value = "Guardar archivo  "
    ruta = notepad.select_folder(title="Guardar archivo en", folder=".")
    archivo = open(str(ruta) + "/demofile.txt", "w")
    archivo.write(texto.value)
    archivo.close()

def file_close():
    estado.value = "Salir  "
    if notepad.yesno("Cerrar", "¿Está seguro de querer salir?"):
        notepad.destroy()

#-- Funciones menu Editar
def edit_function():
    estado.value = "Edit option  "

def wrap_line():
    if (texto.wrap == False):
        texto.wrap = True
    else:
        texto.wrap = False
    estado.value = "Ajuste de línea: " + str(texto.wrap) + "  "

#-- Funciones menu HERRAMIENTAS
def calc():
    pass

def tool2():
    estado.value = "Insertar fecha  "
    fecha = datetime.now()
    texto.append(fecha)

#-- Funciones BARRA DE ESTADO
def count_char():
    tipeado.value = "Tipeado: " + str(len(texto.value)-1)

def cambiar_color():
    rgb_color = opcion_window.select_color()
    texto.text_color = (rgb_color)
    opcion_window.hide()

def cambiar_fuente():
    texto.font = "Arial"

#-- Funciones MENU CONTEXTUAL
def paste():
    texto.tk.event_generate("<<Paste>>")
    estado.value = "Pegar  "

def copy():
    texto.tk.event_generate("<<Copy>>")
    estado.value = "Copiar  "

#-- Ventanas
notepad = App(title="Editor de Textos", layout="auto")
opcion_window = Window(notepad, title="Opciones", width=300, height=150, visible=False)

#-- Layout Notepad
box_texto = Box(notepad, width="fill", height="fill", align="top")
box_barra = Box(notepad, width="fill", align="bottom")

#-- Widgets Notepad
menubar = MenuBar(notepad,
            toplevel=["Archivo", "Editar", "Herramientas"],
            options=[
                        [ ["Abrir archivo", file_open], ["Guardar", file_save], ["Salir", file_close]],
                        [ ["Copiar", edit_function], ["Pegar", edit_function] , ["Ajuste de línea", wrap_line]],
                        [ ["Calculadora", calc], ["Insertar Fecha/Hora", tool2]]
                    ])

texto = TextBox(box_texto, width="fill", height="fill", command=count_char, 
        multiline=True, scrollbar=True)
texto.font = "Courier"
texto.text_size = 12

tipeado = Text(box_barra, size=10, text="Tipeado: ", align="left")
estado = Text(box_barra, size=10, align="right")

#-- Widget Menu() de Tkinter (Menu Contextual)
menu_contextual = Menu(box_texto.tk, tearoff = 0)
menu_contextual.add_command(label ="Pegar", command=paste)
menu_contextual.add_command(label ="Copiar", command=copy)
menu_contextual.add_separator()
menu_contextual.add_command(label ="Buscar")

#-- Widgets Ventana Opciones
texto_opciones = Text(opcion_window, text="Cambiar el color del texto:")
elegir_color = PushButton(opcion_window, width=50, height=50, image="./icons/font_c.png", command=cambiar_color)
elegir_fuente = PushButton(opcion_window, width=50, height=50, image="./icons/font.png", command=cambiar_fuente)

#-- Eventos
box_barra.when_right_button_pressed = lambda : opcion_window.show()
texto.when_right_button_pressed = lambda event : menu_contextual.tk_popup(event.display_x, event.display_y)
notepad.when_closed = file_close

notepad.display()
