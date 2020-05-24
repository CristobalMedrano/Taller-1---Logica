import tkinter as tkinter
from tkinter import *
from tkinter import messagebox
import time as tm

def clicked():
    if(text_name.get() != ""):
        name_user = text_name.get()
        #new_window = tkinter.Toplevel(main_window)
        new_window = Tk()
        main_window.destroy()
        new_window.mainloop()
        
    else:
        messagebox.showerror(title="Error", message= "Debes ingresar el nombre del paciente antes de continuar")
    

main_window=Tk()

name_user = ""

main_window.title("LogicDoctor")
main_window.geometry("600x300+0+0")
main_window.resizable(width=False, height=False)

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

label_collaborators = tkinter.Label(text="Ingrese el nombre del paciente")
label_collaborators.place(x=380, y=200)

text_name = tkinter.Entry(main_window, width=15)
text_name.place(x=380, y=233)

button_begin = tkinter.Button(text="Comenzar", command = clicked)
button_begin.place(x=480, y=230)


    
		
main_window.mainloop()
