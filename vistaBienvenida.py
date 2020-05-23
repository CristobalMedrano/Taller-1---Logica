import tkinter as tkinter
from tkinter import *

main_window=Tk()

main_window.title("LogicDoctor")
main_window.geometry("600x300+0+0")
#main_window.config(bg="blue")

photo= PhotoImage(file="imagen.png")
label_photo = tkinter.Label(main_window, image=photo).place(x=0,y=0)
        
label_title = tkinter.Label(main_window,text="Logic Doctor App")
label_title.place(x=220, y=20)
label_title.config(font=(28))

label_description = tkinter.Label(text="Hola, soy un sistema de asesoramiento que simula un diagnostico medico, \npara esto necesito que selecciones los sintomas que presenta el paciente \npara determinar la posible afeccion medica.")
label_description.place(x=80, y=70)

label_information = tkinter.Label(text="INFORMACION IMPORTANTE: \nLogic Doctor App tiene un fin exclusivamente informativo, si el paciente \ncree que los sintomas son graves debe recurrir a su medico mas cercano.")
label_information.place(x=80, y=140)

label_collaborators = tkinter.Label(text="Autores: \n - Jorge Ayala\n - Felipe Gonzalez\n - Cristobal Medrano\n - Javier Perez")
label_collaborators.place(x=30, y=200)

button_begin = tkinter.Button(text="Comenzar")
button_begin.place(x=480, y=230)
		
main_window.mainloop()
