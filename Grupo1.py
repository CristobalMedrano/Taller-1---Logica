from pyswip import Prolog, Query
import os.path as path
from collections import Counter
from time import time
import tkinter as tk
import random

global user_symptoms, btn_top_symptoms_list, lbl_init_symptoms, lbl_current_symptoms
p = Prolog()

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

def is_valid_file(filename):
    if not path.exists(filename):
        return False
    elif filename[-4:] != ".txt":
        return False
    else:
        return True

def filter_line(line):
    return line.replace("\t", "").replace("\n", "").split(' _ ')

def add_pathology(disease, symptom):
    pathology = "pathology('"+disease+"','"+symptom+"')"
    p.assertz(pathology)

def show_all_pathology():
    for soln in p.query("pathology(Disease, Symptom)"):
        print("[Pathology] "+soln["Disease"]+": "+soln["Symptom"])

def get_all_disease():
    disease = []
    for soln in p.query("pathology(Disease, Symptom)"):
        disease.append(soln["Disease"])
    return disease

def is_pathology(disease, symptom):
    query = "pathology('"+disease+"','"+symptom+"')"
    response = list(p.query(query))
    return is_valid_query(response)

def diseases_by_symptom(symptom):
    query = "pathology(Disease,'"+symptom+"')"
    response = prolog_query(query)
    return response

def symptoms_by_disease(disease):
    query = "pathology('"+disease+"', Symptom)"
    response = prolog_query(query)
    return response

def prolog_query(query):
    p_query = list(p.query(query))
    if is_valid_query(p_query):
        response = query_results(p_query)
    else:
        response = []
    return response

def is_valid_query(query):
    if query == []:
        return False
    else:
        return True

def query_results(query_response):
    name = get_query_name(query_response)
    response = []
    for res in query_response:
        response.append(res[name])
    return response

def get_query_name(query_response):
    return [*query_response[0]][0]

def diseases_by_symptoms(symptoms):
    diseases = []
    for symptom in symptoms:
        res = diseases_by_symptom(symptom)
        for disease in res:
            diseases.append(disease)
    diseases = disease_filter(diseases, symptoms)
    return diseases

def disease_filter(diseases, symptoms):
    common_diseases = Counter(diseases).items()
    diseases_filter = filter_common_diseases(symptoms, common_diseases)
    diseases = get_counter_names(diseases_filter)
    return diseases

def filter_common_diseases(symptoms, common_diseases):
    return list(filter(lambda disease: match(disease, symptoms), common_diseases))

def match(disease, symptoms):
    count_disease = disease[1]
    len_symtoms = len(symptoms)
    if count_disease == len_symtoms:
        return True
    else:
        return False

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

#la funcion retorna el numero de sintomas que uno desea (number_symptoms) en base a una lista de enfermedades (diseases)
def top_symptoms(number_symptoms,diseases):
    symptoms = []
    repetitions = []
    top_symptoms_return = []
    for disease in diseases:
        symptoms += symptoms_by_disease(disease)
    for symptom in symptoms:
        repetitions.append(symptoms.count(symptom))
    bubble_order(repetitions,symptoms)
    for symptom in symptoms:
        if top_symptoms_return.count(symptom) == 0 and user_symptoms.count(symptom) == 0:
            top_symptoms_return.append(symptom)
            if len(top_symptoms_return) == number_symptoms:
                return top_symptoms_return
    return top_symptoms_return

def top_symptoms_2(number_symptoms, diseases):
    all_symptoms = []
    for disease in diseases:
        for symptom in symptoms_by_disease(disease):
            if not symptom in user_symptoms:
                all_symptoms.append(symptom)
    symptoms = symptom_filter(number_symptoms, all_symptoms)
    return symptoms

def symptom_filter(number_symptoms, symptoms):
    common_symptoms = Counter(symptoms).most_common(number_symptoms)
    return get_counter_names(common_symptoms)

def get_counter_names(counter_common):
    return list(map(lambda name: name[0], counter_common))

def bubble_order(listRepetitions,listSymptoms):
    for dato in range(len(listRepetitions)-1,0,-1):
        for i in range(dato):
            if listRepetitions[i]<listRepetitions[i+1]:
                temp = listRepetitions[i]
                temp2 = listSymptoms[i]
                listRepetitions[i] = listRepetitions[i+1]
                listSymptoms[i] = listSymptoms[i+1]
                listRepetitions[i+1] = temp
                listSymptoms[i+1] = temp2

def gui_disease():
    pass

def hola(symptom):
    global user_symptoms
    if not symptom.lower() in user_symptoms:
        user_symptoms.append(symptom.lower())
    print(top_symptoms_2(10, diseases_by_symptoms(user_symptoms)))
    #print(diseases_by_symptoms(user_symptoms))

def update_lbl_current_symptoms(symptom):
    global lbl_current_symptoms
    lbl_current_symptoms["text"] = lbl_current_symptoms["text"]+ "\n" + symptom.capitalize() + "\n"

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

'''
from tkinter import *destroy

root = Tk()

b = Button(root, text="Delete me", command=b.forget)
b.pack()

b['command'] = b.forget

root.mainloop()
'''

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

def update():
    l.config(text=str(random.random()))
    root.after(1000, update)

#root = tk.Tk()
#l = tk.Label(text='0')
#l.pack()
#root.after(1000, update)
#root.mainloop()

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
main()