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

def check_response(query):
    if query == []:
        return False
    else:
        return True

def disease_by_symptom(symptom):
    query = "pathology(Disease,'"+symptom+"')"
    prolog_query = list(p.query(query))
    response = query_results(prolog_query)
    return response

def symptom_by_disease(disease):
    query = "pathology('"+disease+"', Symptom)"
    prolog_query = list(p.query(query))
    response = query_results(prolog_query)
    return response

def is_pathology(disease, symptom):
    query = "pathology('"+disease+"','"+symptom+"')"
    response = list(p.query(query))
    return check_response(response)

def query_results(query_response):
    name = get_query_name(query_response)
    response = []
    for res in query_response:
        response.append(res[name])
    return response

def get_query_name(query_response):
    return [*query_response[0]][0]

def main():
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        response = disease_by_symptom('fiebre')
        print(response)
    else:
        print(False)
main()