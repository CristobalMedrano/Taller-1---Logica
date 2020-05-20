from pyswip import Prolog, Query
import os.path as path

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

def result_disease(query_response):
    if (len(query_response) > 3):
        print("Aun existen muchas enfermedades, por favor siga seleccionando sintomas para tener un resultado mas exacto")
        return False
    elif (len(query_response) == 0):
        print("Con los sintomas entregados no se encontro ninguna solucion, por favor vuelva a intentarlo")
        return False
    else:
        print("Los sintomas encontrados son:")
        print(query_response)
        return True

def main():
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        response = diseases_by_symptom('tos')
        response_2 = diseases_by_symptom('tos2')
        response_3 = diseases_by_symptom('piel seca')
        print(response, response_2)
        result_disease(response)
        result_disease(response_2)
        result_disease(response_3)
    else:
        print(False)
main()