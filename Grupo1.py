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

def view_all_pathology():
    for soln in p.query("pathology(Disease, Symptom)"):
        print("[Pathology] "+soln["Disease"]+": "+soln["Symptom"])
# Query Example
#testQuery = list(prolog.query('index("urticaria por frio","un empeoramiensto de la reaccion a medida que la piel se calienta")'))
#if testQuery == []:
#    print(False)
#else:
#    print(True)

def main():
    read_file = read_pathology_file("pathology.txt")
    if read_file is True:
        #view_all_pathology()
        print(True)
    else:
        print(False)
main()