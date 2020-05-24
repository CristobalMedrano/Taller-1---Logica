from tkinter import *
from tkinter import ttk, font

#prueba = ['tos', 'fiebre', 'mucosidad', 'escalofrios','fatiga']
prueba = ['tos', 'fiebre', 'mucosidad', 'escalofrios']
#prueba = ['tos']

def returnName(name,symptomsList):
    symptomsList.append(name)
    print(name)

symptoms = []

raiz = Tk()
# Titulo.
raiz.title("Doctor")
# Formato.
fuente = font.Font(weight='bold')
# Tamaño
raiz.geometry("500x287")
# Se agregan botones.
contador = 0
while contador < len(prueba):
    name = prueba[contador]
    ttk.Button(raiz, text=name, command=lambda j=name: returnName(j,symptoms)).pack(padx=10, pady=10)
    contador = contador + 1

raiz.mainloop()
    
print(symptoms)