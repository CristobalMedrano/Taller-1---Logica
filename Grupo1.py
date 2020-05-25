from pyswip import Prolog, Query
import os.path as path
from collections import Counter
from time import time
from tkinter import messagebox
import tkinter as tk
import random

global  user_symptoms, btn_top_symptoms_list, lbl_init_symptoms, lbl_current_symptoms, text_name, main_window, lbl_possible_disease, user_frame_disease, user_top_symptoms, btn_no_symptoms
p = Prolog()

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, bg="white")
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, height = 550, bg="white")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas, bg="white")
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

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

def len_symptoms(diseases):
    all_symptoms = []
    for disease in diseases:
        for symptom in symptoms_by_disease(disease):
            if not symptom in all_symptoms:
                all_symptoms.append(symptom)
    return len(all_symptoms)

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

def top_symptoms_3(diseases):
    all_symptoms = []
    for disease in diseases:
        for symptom in symptoms_by_disease(disease):
            if not symptom in user_symptoms:
                all_symptoms.append(symptom)
    symptoms = symptom_filter_3(all_symptoms)
    return symptoms

def symptom_filter_3(symptoms):
    common_symptoms = list(filter( lambda symptom: symptom[1] >= 10, Counter(symptoms).most_common()))
    return get_counter_names(common_symptoms)

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

def update_btn_symptoms():
    print(diseases_by_symptoms(user_symptoms))
    i = 0
    remaining_symptoms = top_symptoms_2(top, diseases_by_symptoms(user_symptoms))
    print(remaining_symptoms)
    for nombre in remaining_symptoms:
        btn_top_symptoms_list[i]["text"] = nombre.capitalize()
        i += 1
    while i < top:
        btn_top_symptoms_list[i].destroy()
        '''btn_top_symptoms_list[i]["text"] = ""
        btn_top_symptoms_list[i]["state"] = tk.DISABLED
        btn_top_symptoms_list[i]["bg"] = "white"
        btn_top_symptoms_list[i]["bd"] = "0"'''
        i += 1

def lbl_end_disease():
    diseases = diseases_by_symptoms(user_symptoms)
    if len(diseases) > 1:
        ##
        ## aqui bloquea los botones o los borra
        ##
        i = 0
        while i < top:
            btn_top_symptoms_list[i]["state"] = tk.DISABLED
            i += 1
        msg_diseases = ""
        for disease in diseases:
            lbl_possible_disease["text"] = lbl_possible_disease["text"] + "\n" + disease.capitalize() + "\n"
            msg_diseases = msg_diseases + disease +"\n"
        messagebox.showwarning(title="DIAGNOSTICO", message= "Con la cantidad de síntomas ingresados, nuestro diagnostico no puede ser certero. \nA continuación te mostraremos las posibles patologías que puedes tener, según nuestros registros." , parent=user_frame_disease)

    else:
        i = 0
        while i < top:
            btn_top_symptoms_list[i]["state"] = tk.DISABLED
            i += 1
        lbl_possible_disease["text"] = lbl_possible_disease["text"] + "\n" + diseases[0].capitalize() + "\n"
        messagebox.showinfo(title="DIAGNOSTICO", message= "Los sintomas ingresados pueden ser de "+ diseases[0], parent=user_frame_disease)
    btn_no_symptoms["state"] = tk.DISABLED

def btn_symptom_action(btn):
    global user_symptoms, top
    symptom = btn['text'].lower()
    if not symptom in user_symptoms:
        user_symptoms.append(symptom)
        update_lbl_current_symptoms(symptom)
    update_btn_symptoms()
    top = len(top_symptoms_2(top, diseases_by_symptoms(user_symptoms)))
    print('La cantidad de botones que hay son:'+str(togp))
    if btn_no_symptoms["state"] == tk.DISABLED and user_symptoms != []:
        btn_no_symptoms["state"] = tk.NORMAL

    if result_disease(diseases_by_symptoms(user_symptoms), 1) or len(user_symptoms) == 0:
        lbl_init_symptoms["text"] = "Usted además puede presentar\n algunos de estos síntomas."
        lbl_end_disease()
    else:
        lbl_init_symptoms["text"] = "Necesito más síntomas para \nhacer el diagnóstico.\n ¿Presenta alguno de estos síntomas?"
        
def start_program(init_top_symptoms, top):
    if(text_name.get() != ""):
        global btn_top_symptoms_list, lbl_init_symptoms, lbl_current_symptoms, lbl_possible_disease, window, main_window, user_frame_disease, user_top_symptoms, btn_no_symptoms
        name_user = text_name.get()
        #new_window = tkinter.Toplevel(main_window)
        window = tk.Tk(className='Taller 1 - Dr LPO')

        main_window.destroy()
        window.configure(bg="white")
        window.resizable(False, False)
        user_frame = tk.Frame(master=window, width=1200, height=100, bg="#7ac5cd")
        exit_program = tk.Frame(master=window, width=1200, height=50, bg="#7ac5cd")
        user_top_symptoms = tk.Frame(master=window, width=400, height=620, bg="white")
        user_current_symptoms = tk.Frame(master=window, width=400, bg="white")
        aux_frame = tk.Frame(master=window, width=1, bg="black")
        aux_frame_2 = tk.Frame(master=window, width=1, bg="black")
        user_frame_disease = tk.Frame(master=window, width=400, bg="white")

        scframe = VerticalScrolledFrame(user_top_symptoms)
        scframe.pack()
        #scrollbar = Scrollbar(root)
        #scrollbar.pack( side = RIGHT, fill = Y )

        lbl_user_name = tk.Label(
            master=user_frame,
            text="Paciente: "+name_user,
            bd=2,
            fg="white",
            bg="#7ac5cd", 
            font=("Arial", 14)
            )
        lbl_user_name.grid(row=0, column=0, padx=20, pady=10)



        lbl_init_symptoms = tk.Label(
            master=scframe.interior,
            text="¿Presenta alguno de estos síntomas?",
            bg="white",
            font=("Arial", 14)
        )
        lbl_init_symptoms.grid(row=0, column=0, padx=20, pady=10)

        btn_top_symptoms_list = []
        i = 1
        for symptom in init_top_symptoms:

            btn_top_symptom = tk.Button(
                master=scframe.interior,
                text=symptom.capitalize(),
                font=("Arial", 14),
                bd=2,
                fg="white",
                bg="#7ac5cd",
                state=tk.NORMAL,
                width=30
            )
            btn_top_symptom["command"] = lambda btn=btn_top_symptom: btn_symptom_action(btn)
            btn_top_symptom.grid(row=i, column=0, pady=5)
            btn_top_symptoms_list.append(btn_top_symptom)
            i += 1
        
        lbl_current_symptoms = tk.Label(
            master=user_current_symptoms,
            text="Sintomas ingresados:\n",
            bg="white",
            font=("Arial", 14)
        )
        lbl_current_symptoms.grid(row=0, column=0, padx=100, pady=10)

        lbl_possible_disease = tk.Label(
            master=user_frame_disease,
            text="Posible patología:\n",
            bg="white",
            font=("Arial", 14)
        )
        lbl_possible_disease.grid(row=0, column=0, padx=20, pady=10)

        btn_exit = tk.Button(master=exit_program, text="Salir", bg="white", font=("Arial", 14), width=10, command= lambda x=window :window.destroy())
        btn_exit.place(x=1075, y=5)
        btn_no_symptoms = tk.Button(master=exit_program, state=tk.DISABLED, text="No, no presento más sintomas", bg="white", font=("Arial", 14), width=30, command= lambda x=1 :lbl_end_disease())
        btn_no_symptoms.place(x=20, y=5)
        #lbl_current_symptoms["text"] = lbl_current_symptoms["text"]+"hola amigos"

        user_frame.pack(fill=tk.X, side=tk.TOP)
        exit_program.pack(fill=tk.X, side=tk.BOTTOM)
        user_top_symptoms.pack(fill=tk.BOTH, side=tk.LEFT, pady=10, padx=10)
        aux_frame.pack(fill=tk.Y, side=tk.LEFT, pady=15 ,padx=10)
        user_current_symptoms.pack(fill=tk.BOTH, side=tk.LEFT,  pady=10)
        aux_frame_2.pack(fill=tk.Y, side=tk.LEFT, pady=15 ,padx=10)
        user_frame_disease.pack(fill=tk.BOTH, side=tk.LEFT, pady=10)


        window.mainloop()
        
    else:
        messagebox.showerror(title="Error", message= "Debes ingresar el nombre del paciente antes de continuar", parent="")

def main():
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        global user_symptoms, text_name, main_window, top
        user_symptoms = []
        start_time = time()
        all_diseases = get_all_disease()
        elapsed_time = time() - start_time
        print("Elapsed time: %.10f seconds." % elapsed_time)
        #print(top_symptoms(10, all_diseases))
        #elapsed_time = time() - start_time - elapsed_time
        #print("Elapsed time: %.10f seconds." % elapsed_time)
        #print(top_symptoms_2(175, all_diseases))
        elapsed_time = time() - start_time - elapsed_time
        print("Elapsed time: %.10f seconds." % elapsed_time)

        # Top symptoms
        top = len(top_symptoms_3(all_diseases))
        init_top_symptoms = top_symptoms_2(top, all_diseases)

        main_window=tk.Tk()

        name_user = ""

        main_window.title("LogicDoctor")
        main_window.geometry("800x600")
        main_window.resizable(width=False, height=False)
        photo= tk.PhotoImage(file="fondo.png")
        label_photo = tk.Label(main_window, image=photo).place(x=0,y=0)
                
        label_title = tk.Label(main_window,text="Logic Doctor App", bg="white", font=("Arial", 28))
        label_title.place(x=400, y=20)

        label_description = tk.Label(text="Hola, soy un sistema de asesoramiento que simula un\n diagnostico medico, para esto\n necesito que selecciones\n los sintomas que presenta el paciente \npara determinar la posible afección médica.", font=("Arial", 14), bg="#fcfbfb")
        label_description.place(x=320, y=80)

        label_information = tk.Label(text="INFORMACION IMPORTANTE: \nLogic Doctor App NO RECOMIENDA SU USO PARA \nFINES PROFESIONALES, esta App se creó\n con fines estudiantiles y en ningún caso deben\n tomarse en cuenta los resultados obtenidos aquí.", font=("Arial", 14), bg="#fcfbfb")
        label_information.place(x=320, y=220)

        label_collaborators = tk.Label(text="Desarrollado por: \n - Jorge Ayala\n - Felipe Gonzalez\n - Cristobal Medrano\n - Javier Perez", font=("Arial", 14), bg="#fefefe")
        label_collaborators.place(x=30, y=460)

        label_collaborators = tk.Label(text="Para continuar, ingrese el nombre del paciente.", font=("Arial", 14), bg="#fcfcfc")
        label_collaborators.place(x=350, y=500)

        text_name = tk.Entry(main_window, width=40)
        text_name.place(x=400, y=540)

        button_begin = tk.Button(text="Comenzar",font=("Arial", 14), width=10, command = lambda init=init_top_symptoms:  start_program(init_top_symptoms, top))
        button_begin.place(x=650, y=540)

        main_window.mainloop()

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