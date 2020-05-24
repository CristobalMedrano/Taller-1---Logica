####### BLOQUE DE DEFINICION #######

#### IMPORTACIÓN DE FUNCIONES Y LIBRERÍAS.

from pyswip import Prolog, Query
import os.path as path
from collections import Counter
from time import time
import tkinter as tk
import random

#### DEFINICIÓN DE CONSTANTES Y VARIABLES GLOBALES.

global user_symptoms, btn_top_symptoms_list, lbl_init_symptoms, lbl_current_symptoms
p = Prolog()

#### DEFINICIÓN DE FUNCIONES Y CLASES.


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

# Función que permite leer el archivo de texto pathology_file y cargar su contenido en una base de conocimiento.
# Entrada: String con el nombre del archivo de texto a cargar.
# Salida: Boolean. True o False, dependiendo si el archivo de texto se pudo cargar correctamente.
def read_pathology_file(pathology_file):
    if is_valid_file(pathology_file):
        file = open(pathology_file, 'r')
        for line in file:
            filtered_line = filter_line(line)
            add_pathology(filtered_line[0], filtered_line[1])
        file.close()
        return True
    else:
        return False

# Función que permite verificar si el archivo de texto de entrada existe en la carpeta contenedora del programa.
# Entrada: String con el nombre del archivo de texto a verificar.
# Salida: Boolean. True o False, dependiendo si existe el archivo de texto en el directorio.
def is_valid_file(filename):
    if not path.exists(filename):
        return False
    elif filename[-4:] != ".txt":
        return False
    else:
        return True

# Función que permite formatear la línea leída desde el archivo de entrada, quitanto salto de linea y tabulación.
# Entrada: String que contiene la línea leída.
# Salida: String que contiene la línea formateada.
def filter_line(line):
    return line.replace("\t", "").replace("\n", "").split(' _ ')

# Predicado que permite añadir las patologias del archivo de texto en la base de conocimientos, con la forma del siguiente hecho: "pathology(disease,symptom)"
# Entrada: String que contiene la enfermedad y String que contiene el sintoma respectivo de la enfermedad.
# Salida: Hecho construido y agregado a la base de conocimientos.
def add_pathology(disease, symptom):
    pathology = "pathology('"+disease+"','"+symptom+"')"
    p.assertz(pathology)

# Predicado que permite mostrar todos los hechos presentes en la base de conocimiento.
# Entrada: Vacía.
# Salida: Vacía. Se imprime por pantalla todos las patologías representadas como hechos.
def show_all_pathology():
    for soln in p.query("pathology(Disease, Symptom)"):
        print("[Pathology] "+soln["Disease"]+": "+soln["Symptom"])

# Predicado que permite listar todas las enfermedades presentes en la base de conocimiento.
# Entrada: Vacía.
# Salida: Una lista que contiene todas las enfermedades de la base de conocimiento.
def get_all_disease():
    disease = []
    for soln in p.query("pathology(Disease, Symptom)"):
        disease.append(soln["Disease"])
    return disease

# Predicado que dada una consulta sobre una patología en la base de conocimiento, verifica si la consulta es válida.
# Entrada: String que contiene la enfermedad y String que contiene le síntoma.
# Salida: Boolean. True o False, dependiendo si es la consulta en la base de conocimiento es válida o no.
def is_pathology(disease, symptom):
    query = "pathology('"+disease+"','"+symptom+"')"
    response = list(p.query(query))
    return is_valid_query(response)

# Predicado que dado un sintoma, obtiene una lista de todas las enfermedades que lo contienen.
# Entrada: String que representa al sintoma.
# Salida: Lista que contiene las enfermedades.
def diseases_by_symptom(symptom):
    query = "pathology(Disease,'"+symptom+"')"
    response = prolog_query(query)
    return response

# Predicado que dado una enfermedad, obtiene una lista de los sintomas presentes en dicha enfermedad.
# Entrada: String que representa la enfermedad.
# Salida_ Lista que contiene los sintomas.
def symptoms_by_disease(disease):
    query = "pathology('"+disease+"', Symptom)"
    response = prolog_query(query)
    return response

# Predicado que dada una consulta, verifica si es valida y la transforma en formato lista.
# Entrada: Consulta en la base de conocimiento.
# Salida: Respuesta de la consulta.
def prolog_query(query):
    p_query = list(p.query(query))
    if is_valid_query(p_query):
        response = query_results(p_query)
    else:
        response = []
    return response

# Predicado que dada una consulta, verifica si está entrega un respuesta vacía o no.
# Entrada: Consulta en la base de conocimiento.
# Salida: Boolean. True o False, dependiendo si la consulta obtuvo una respuesta o no.
def is_valid_query(query):
    if query == []:
        return False
    else:
        return True

# Predicado que dada una respuesta a una consulta en la base de conocimientos, lista dicha respuesta.
# Entrada: Respuesta de consulta en la base de conocimiento.
# Salida: Lista que contiene el resultado de la consulta.
def query_results(query_response):
    name = get_query_name(query_response)
    response = []
    for res in query_response:
        response.append(res[name])
    return response

# Predicado que dada una respuesta a una consulta en la base de conocimientos, obtiene el nombre de dicha consulta.
# Entrada: Respuesta de consulta en la base de conocimiento.
# Salida: String que contiene el nombre de dicha consulta.
def get_query_name(query_response):
    return [*query_response[0]][0]

# Predicado que dada una lista de síntomas, obtiene las enfermedades en donde estan presentes los sintomas ingresados.
# Entrada: Lista de String que contiene cada sintoma a consultar.
# Salida: Lista de enfermedades.
def diseases_by_symptoms(symptoms):
    diseases = []
    for symptom in symptoms:
        res = diseases_by_symptom(symptom)
        for disease in res:
            diseases.append(disease)
    diseases = disease_filter(diseases, symptoms)
    return diseases

# Predicado que permite filtrar las enfermedades. 
# Entrada: Lista de String que contiene enfermedades y Lista de String que contiene síntomas.
# Salida: Lista con de String con las enfermedades filtradas.
def disease_filter(diseases, symptoms):
    common_diseases = Counter(diseases).items()
    diseases_filter = filter_common_diseases(symptoms, common_diseases)
    diseases = get_counter_names(diseases_filter)
    return diseases

# Predicado que permite contar y filtrar las enfermedades ingresadas.
# Entrada: Lista de String que contiene las enfermedades repetidas y una Lista con los respectivos síntomas.
# Salida: Lista de String con las enfermedades filtradas.
def filter_common_diseases(symptoms, common_diseases):
    return list(filter(lambda disease: match(disease, symptoms), common_diseases))

# Función que tiene la condición de filtrado para los sintomas de una enfermedad.
# Entrada: Lista de String que contiene enfermedades y Lista de String que contiene los síntomas.
# Salida: Boolean. True o False, dependiendo si se cumplió o no la condición del filtrado.
def match(disease, symptoms):
    count_disease = disease[1]
    len_symtoms = len(symptoms)
    if count_disease == len_symtoms:
        return True
    else:
        return False

# Condición para verificar si es necesario parar la lógica del programa.
# Entrada: Lista de String que contiene las posibles enfermedades del usuario e Integer top que permite saber en que momento hacer el corte del programa.
# Salida: Bool. True o False, dependiendo si el usuario ha cumplido la condición necesaria par terminar el programa.
def result_disease(query_response, top):
    if (len(query_response) > top):
        print("Aun existen muchas enfermedades, por favor siga seleccionando sintomas para tener un resultado mas exacto")
        return False
    elif (len(query_response) == 0):
        print("Con los sintomas entregados no se encontro ninguna solucion, por favor vuelva a intentarlo")
        return False
    else:
        print("Los sintomas encontrados son:")
        print(query_response)
        return True
 
# Predicado que dado una lista de enfermedades y una cantidad N, permite obtener los N sintomas más comunes entre las enfermedades de entrada.
# Entrada: Integer que indica cuantos sintomas mostrará el top y Lista con las enfermedades de donde se obtendran los sintomas.
# Salida: Lista de String que contiene los sintomas más comunes entre las enfermedades ingresadas.
def top_symptoms_2(number_symptoms, diseases):
    all_symptoms = []
    for disease in diseases:
        for symptom in symptoms_by_disease(disease):
            if not symptom in user_symptoms:
                all_symptoms.append(symptom)
    symptoms = symptom_filter(number_symptoms, all_symptoms)
    return symptoms

# Predicado que permite filtrar los sintomas. 
# Entrada: Lista de String que contiene enfermedades y Lista de String que contiene síntomas.
# Salida: Lista con de String con los sintomas filtrados.
def symptom_filter(number_symptoms, symptoms):
    common_symptoms = Counter(symptoms).most_common(number_symptoms)
    return get_counter_names(common_symptoms)

# Predicado que permite obtener los nombres de un resultado de una consulta a la base de conocimiento.
# Entrada: Lista de String con la respuesta a una consulta, esta respuesta debe estar filtrada.
# Salida: Lista de String con los nombres.
def get_counter_names(counter_common):
    return list(map(lambda name: name[0], counter_common))

# Función que permite actualizar, en la vista principal, los sintomas actuales que presenta el usuario.
# Entrada: Lista que contiene los sintomas actuales.
# Salida: Vacía. Actualiza los labels dentro de la vista principal. 
def update_lbl_current_symptoms(symptom):
    global lbl_current_symptoms
    lbl_current_symptoms["text"] = lbl_current_symptoms["text"]+ "\n" + symptom.capitalize() + "\n"

# No cache que hacia.
def toggleText(btn):
    symptom = btn['text'].lower()
    global user_symptoms
    if not symptom in user_symptoms:
        user_symptoms.append(symptom)
    
    update_lbl_current_symptoms(symptom)

    i = 0
    sintomas_restantes = top_symptoms_2(10, diseases_by_symptoms(user_symptoms))
    largo_del_arreglo = len(sintomas_restantes)
    print(diseases_by_symptoms(user_symptoms))
    for nombre in sintomas_restantes:
        btn_top_symptoms_list[i]["text"] = nombre.capitalize()
        #btn_top_symptoms_list[i]["text"] = str(i)
        i += 1

    while i < (10):
        btn_top_symptoms_list[i]["text"] = ""
        btn_top_symptoms_list[i]["state"] = tk.DISABLED
        btn_top_symptoms_list[i]["bg"] = "white"
        i += 1

# Función que pemite crear botones dentro de la vista.
# Entrada: Lista de String con el top de los sintomas, Lista de String con los sintomas ingresados por el usuario y la ventana enla cual se crearan los botones.
# Salida: Vacía. Crea los botones en la ventana.
def list_button(init_top_symptoms, user_top_symptoms, window):
    i = 1
    for symptom in init_top_symptoms:
        btn_top_symptom = tk.Button(
            master=user_top_symptoms,
            text=symptom.capitalize(),
            font=("Arial", 14),
            bd=0,
            fg="white",
            bg="#7ac5cd",
            activebackground="#619da4",
            state=DISABLED,
            width=30
        )
        btn_top_symptom["command"] = lambda btn=btn_top_symptom: toggleText(btn, window)
        btn_top_symptom.config(cursor='hand2 blue blue') # phew!
        btn_top_symptom.grid(row=i, column=0, padx=10, pady=5)
        i += 1

#Esta no se si la usas.
def update():
    l.config(text=str(random.random()))
    root.after(1000, update)

# Función que permite realizar toda la lógica del programa.
# Realiza la construcción de la vista principal y se encarga de realizar las consultas a la base de conociemiento.
# Muestra, mediante la vista, la respuesta al usuario en caso de encontrar una enfermedad que contemple los sintomas ingresados.
# Entrada: Vacía.
# Salida: Vacía.
def main():
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        global user_symptoms, btn_top_symptoms_list, lbl_init_symptoms, lbl_current_symptoms
        user_symptoms = []
        
        start_time = time()
        all_diseases = get_all_disease()
        elapsed_time = time() - start_time
        print("Elapsed time: %.10f seconds." % elapsed_time)
        #print(top_symptoms(10, all_diseases))
        #elapsed_time = time() - start_time - elapsed_time
        #print("Elapsed time: %.10f seconds." % elapsed_time)
        print(top_symptoms_2(10, all_diseases))
        elapsed_time = time() - start_time - elapsed_time
        print("Elapsed time: %.10f seconds." % elapsed_time)

        # Top symptoms
        top_number = 10
        if user_symptoms == []:
            init_top_symptoms = top_symptoms_2(top_number, all_diseases)
        else:
            init_top_symptoms = top_symptoms_2(top_number, diseases_by_symptoms(user_symptoms))

        window = tk.Tk(className='Taller 1 - Dr LPO')
        window.configure(bg="white")
        window.resizable(False, False)
        user_frame = tk.Frame(master=window, width=1200, height=100, bg="blue")
        menu_frame = tk.Frame(master=window, width=1200, height=50, bg="green")
        user_current_symptoms = tk.Frame(master=window, width=400, height=620, bg="white")
        aux_frame = tk.Frame(master=window, width=1, bg="black")
        user_top_symptoms = tk.Frame(master=window, width=400, bg="white")
        aux_frame_2 = tk.Frame(master=window, width=1, bg="black")
        frame3 = tk.Frame(master=window, width=400, bg="white")

        lbl_init_symptoms = tk.Label(
            master=user_top_symptoms,
            text="¿Presenta alguno de estos síntomas?",
            bg="white",
            font=("Arial", 14)
        )
        lbl_init_symptoms.grid(row=0, column=0, padx=20, pady=10)

        btn_top_symptoms_list = []
        i = 1
        for symptom in init_top_symptoms:

            btn_top_symptom = tk.Button(
                master=user_top_symptoms,
                text=symptom.capitalize(),
                font=("Arial", 14),
                bd=0,
                fg="white",
                bg="#7ac5cd",
                state=tk.NORMAL,
                width=30
            )
            btn_top_symptom["command"] = lambda btn=btn_top_symptom: toggleText(btn)
            btn_top_symptom.grid(row=i, column=0, padx=10, pady=5)
            btn_top_symptoms_list.append(btn_top_symptom)
            i += 1
        
        lbl_current_symptoms = tk.Label(
            master=user_current_symptoms,
            text="Sintomas ingresados:\n",
            bg="white",
            font=("Arial", 14)
        )
        lbl_current_symptoms.grid(row=0, column=0, padx=20, pady=10)

        #lbl_current_symptoms["text"] = lbl_current_symptoms["text"]+"hola amigos"

        user_frame.pack(fill=tk.X, side=tk.TOP)
        menu_frame.pack(fill=tk.X, side=tk.BOTTOM)
        user_current_symptoms.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=10)
        aux_frame.pack(fill=tk.Y, side=tk.LEFT, expand=True, pady=15 ,padx=0.1)
        user_top_symptoms.pack(fill=tk.BOTH, side=tk.LEFT, expand=True,  pady=10)
        aux_frame_2.pack(fill=tk.Y, side=tk.LEFT, expand=True, pady=15 ,padx=0.1)
        frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        window.mainloop()
        '''
        # Ejemplo de codigo para encontrar una enfermedad.
        response = diseases_by_symptoms(['tos', 'fiebre', 'mucosidad', 'escalofrios'])
        print(diseases_by_symptom('tos'))
        print(diseases_by_symptom('fiebre'))
        print()
        print(top_symptoms(15, ['bronquitis', 'difteria', 'covid-19']))
        print(symptoms_by_disease('bronquitis'))
        print(symptoms_by_disease('difteria'))
        print(symptoms_by_disease('covid-19'))
        print(response )
        start_time = time()
        print(user_symptoms)
        enfermedades = diseases_by_symptoms(user_symptoms)
        print(enfermedades)
        print(top_symptoms(5, enfermedades))
        print(result_disease(enfermedades, 2))
        elapsed_time = time() - start_time
        print("Elapsed time: %.10f seconds." % elapsed_time)
           #la funcion necesita una lista de sintomas como entrada y 
                                                # retorna una lista de enfermedades que comparten esos sintomas.
        # fin del ejemplo'''
    else:
        print(False)

####### BLOQUE PRINCIPAL #######

#### LLAMADO FUNCIÓN MAIN PARA ARRANCAR EL PROGRAMA.
main()