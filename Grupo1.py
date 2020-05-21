from pyswip import Prolog, Query
import os.path as path
from collections import Counter

p = Prolog()

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
    diseases = get_diseases_name(diseases_filter)
    return diseases

def filter_common_diseases(symptoms, common_diseases):
    return list(filter(lambda disease: match(disease, symptoms), common_diseases))

def get_diseases_name(diseases_filter):
    return list(map(lambda disease: disease[0], diseases_filter))
    
def match(disease, symptoms):
    count_disease = disease[1]
    len_symtoms = len(symptoms)
    if count_disease == len_symtoms:
        return True
    else:
        return False

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
        if top_symptoms_return.count(symptom) == 0:
            top_symptoms_return.append(symptom)
            if len(top_symptoms_return) == number_symptoms:
                return top_symptoms_return

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

def main():
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        # Ejemplo de codigo para encontrar una enfermedad.
        response = symptoms_by_disease('faringitis')
        print(diseases_by_symptoms(response))   #la funcion necesita una lista de sintomas como entrada y 
                                                # retorna una lista de enfermedades que comparten esos sintomas.
        # fin del ejemplo

        #Ejemplo de codigo para encontrar el top de sintomas de una lista de enefermedades
        numero_de_sintomas_top = 5
        print(diseases_by_symptoms(['fiebre','tos']))
        print(top_symptoms(numero_de_sintomas_top,diseases_by_symptoms(['fiebre','tos'])))
        #fin del ejemplo
        response = diseases_by_symptom('tos')
        response_2 = diseases_by_symptom('tos2')
        print(response, response_2)
    else:
        print(False)
main()