import requests
import re
import os

site1 = r"https://sites.google.com/site/fiipythonprogramming/laboratories"

def get_function_name(txt):
    functions = re.findall("(The \w+ function)|(the \w+ function)|(function called \w+)|(o funcție <span[^>]*><strong>\w+)", txt)
    functii = []
    #separ numele functiei de restul cuvintelor il pun in lista
    for f in functions:
        for t in f:
            if t != '':
                j = t.split(" ")
                if t[0] == 'T' or t[0] == 't':
                    print(j[1])
                    functii.append(j[1])
                else:
                    print(j[2])
                    functii.append(j[2])
    return functii

#returneaza 1 daca exista denumiri de functii in enunt si 0 altfel
def check_for_function_names(txt):
    functions = re.findall("(The \w+ function)|(the \w+ function)|(function called \w+)|(o funcție <span[^>]*><strong>\w+)", txt)
    g = 0
    for f in functions:
        for t in f:
            if t != '':
                g = 1
    return g


def create_file(lab_no, path):

    r = requests.get(site1 + '/' + lab_no)
    r.raise_for_status()
    html_content = r.text

    exercices = re.findall("(<p dir=\"ltr\"[^>]*>(\s)*(\d)(\d)?[\.|)][^<]*)", html_content)

    it = 1
    #creez fisierul .py
    f = open(os.path.join(path, lab_no + '.py'), 'w')
    print("Fisierul % s.py a fost creat" % lab_no)

    #pentru fiecare exercitiu scriu functiile
    for ex in exercices:
        function = 'def ex' + str(it) + '(parametri):\n\tpass\n'
        if check_for_function_names(ex[0]) == 0: #daca nu exista nume de functie in enunt functia va primi un nume de tipul ex3
            f.write(function)
        else:
            functie = get_function_name(ex[0])
            #definim functia cu numele dat
            function = 'def ' + functie[0] + '(parametri):\n\tpass\n'
            comment = '#ex' + str(it) + '\n'
            f.write(comment)
            f.write(function)
        #print(ex)

        it += 1
    print(it)
    if it == 1:
        exercices = re.findall("(<p dir=\"ltr\" [^>]*>[A-Z][^<]*)", html_content)
        for ex in exercices:
            function = 'def ex' + str(it) + '(parametru):\n\tpass\n'
            if check_for_function_names(ex) == 0:
                f.write(function)
            else:
                functie = get_function_name(ex)
                function = 'def ' + functie[0] + '(parametru):\n\tpass\n'
                comment = '#ex' + str(it) + '\n'
                f.write(comment)
                f.write(function)
            it += 1
            #print(ex)
        print(it)
    f.close()


def create_directories(dir):
    r = requests.get(site1)
    r.raise_for_status()
    html_content = r.text
    lab_links = re.findall('<a.*?href="([^"]+)"[^>]+>\s*Lab \d+', html_content) #linkurile laboratoarelor
    for i in lab_links:
        j = i.split("/") #despart dupa / si iau ultimul cuvant care va fi chiar numarul laboratorului
        lab_no = ""
        for ii in j:
            lab_no = ii
        path = os.path.join(dir, lab_no)
        os.mkdir(path)
        print("Directorul % s a fost creat" % lab_no)
        create_file(lab_no, path)


if __name__ == '__main__':
    d = "F:/Desktop/PythonCrawler"
    direct = input()
    create_directories(direct)