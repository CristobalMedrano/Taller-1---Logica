from pyswip import Prolog, Query
import os.path as path
from collections import Counter
from time import time

global user_symptoms
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

def get_all_pathology():
    pathology = []
    for soln in p.query("pathology(Disease, Symptom)"):
        pathology.append(soln["Disease"])
    return pathology

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
    global user_symptoms
    user_symptoms = ['fiebre', 'tos', 'mucosidad']
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        # Ejemplo de codigo para encontrar una enfermedad.
        response = diseases_by_symptoms(['tos', 'fiebre', 'mucosidad', 'escalofrios'])
        '''print(diseases_by_symptom('tos'))
        print(diseases_by_symptom('fiebre'))
        print()
        print(top_symptoms(15, ['bronquitis', 'difteria', 'covid-19']))
        print(symptoms_by_disease('bronquitis'))
        print(symptoms_by_disease('difteria'))
        print(symptoms_by_disease('covid-19'))'''
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
        # fin del ejemplo
    else:
        print(False)
main()