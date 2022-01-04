import requests
import re
import os

site1 = r"https://sites.google.com/site/fiipythonprogramming/laboratories"
site2 = r"https://sites.google.com/site/fiipythonprogramming/"


def get_function_name(txt):
    functions = re.findall(
        "(The \w+ function)|(the \w+ function)|(function called \w+)|(o funcție <span[^>]*><strong>\w+)", txt)
    g = 0
    functii = []
    it = 0
    for f in functions:
        for t in f:
            #print('--------------------------------------', f)
            if t != '':
                j = t.split(" ")
                if t[0] == 'T' or t[0] == 't':
                    print(j[1])
                    functii.append(j[1])
                    it += 1
                else:
                    print(j[2])
                    functii.append(j[2])
                    it += 1
    return functii


def check_for_function_names(txt):
    functions = re.findall(
        "(The \w+ function)|(the \w+ function)|(function called \w+)|(o funcție <span[^>]*><strong>\w+)", txt)
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
    f = open(os.path.join(path, lab_no + '.py'), 'w')
    print("Fisierul % s.py a fost creat" % lab_no)

    for ex in exercices:
        function = 'def ex' + str(it) + '(parametri):\n\tpass\n'
        if check_for_function_names(ex[0]) == 0:
            f.write(function)
        else:
            functie = get_function_name(ex[0])
            function = 'def ' + functie[0] + '(parametri):\n\tpass\n'
            comment = '#ex' + str(it) + '\n'
            f.write(comment)
            f.write(function)
        print(ex)

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
            print(ex)
        print(it)
    f.close()


def create_directories(dir):
    r = requests.get(site1)
    r.raise_for_status()
    html_content = r.text
    lab_links = re.findall('<a.*?href="([^"]+)"[^>]+>\s*Lab \d+', html_content)
    for i in lab_links:
        j = i.split("/")
        lab_no = ""
        for ii in j:
            lab_no = ii
        path = os.path.join(dir, lab_no)
        os.mkdir(path)
        print("Directorul % s a fost creat" % lab_no)
        create_file(lab_no, path)


if __name__ == '__main__':
    dir = "F:/Desktop/PythonCrawler"
    create_directories(dir)
    # create_file('lab-2', dir)
