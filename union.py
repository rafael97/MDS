import  requests
import simplejson as json
import numpy as np
import re
import matplotlib.pyplot as plt
from IPython.html.widgets import interact, interactive, fixed
tokenID = "30401b1161ddb3d0283ae2771d19fdff"
tokenIdCategories = "27575858460aafa18b2cc706a4496c71"


# GLOBAL CONSTANTS
testNames = ['Folder', 'Quiz', 'tareas', 'Foros',' Recursos'," Parciales"," Laboratorios"," Proyectos"," Talleres"]
folders = []
foldersTeacher = []
tareas = []
foros = []
parciales = []
laboratorios = []
proyectos = []
InformePlagio = []
talleres = []
recursos = []
quices = []
infoCursoID = []
infoCursoFullName = []
cursos = []
contenidoCurso = []
activititype = ["","-Solucion","-NotaMaxima","-NotaMinima"]
evidences = []
rootEvidences  = []
courseByCategory = True
categoryId = '2'

#obtener cursos
if courseByCategory :
    r = requests.get("http://localhost/moodle/webservice/rest/server.php?wsfunction=local_moodle_categories_courses&wstoken="+tokenIdCategories+"&moodlewsrestformat=json&categoryid="+categoryId)
else:
    r = requests.get("http://localhost/moodle/webservice/rest/server.php?wsfunction=core_course_get_courses&wstoken="+tokenID+"&moodlewsrestformat=json")

def count_module(j,modname):
    if modname == "forum":
        foros[j] = foros[j] + 1
    if modname == "assign":
        tareas[j] = tareas[j] + 1
    if modname == "resource" or modname == "url" or modname == "label" or modname == "page":
        recursos[j] = recursos[j] + 1
    if modname == "quiz" or "Quiz" in modname:
        quices[j] = quices[j] + 1
    if modname == "folder":
        folders[j] = folders[j] + 1
    if  "Parcial" in modname :
        parciales[j] = parciales[j] + 1
    if "Laboratorio" in modname:
        laboratorios[j] = laboratorios[j] + 1
    if "Proyecto" in modname:
        proyectos[j] = proyectos[j] + 1
    if "Taller" in modname:
        talleres[j] = talleres[j] + 1


def  verify_evidence (numcourse):
    for root in rootEvidences:
        flag = 0
        for e in evidences:
            for t in activititype:
                if root+t == e:
                    flag+=1
            if flag ==3:
                count_module(numcourse, root)

    evidences.clear()
    rootEvidences.clear()

#guardar cursos
for x in range(len(r.json())):
    cursos.append(r.json()[x])


#cursos
for j in range(len(cursos)):
    # generando un espacio en la lista donde se agregaran el conteo total de cada modulo
    folders.append(0)
    tareas.append(0)
    foros.append(0)
    recursos.append(0)
    quices.append(0)
    parciales.append(0)
    laboratorios.append(0)
    proyectos.append(0)
    talleres.append(0)
    InformePlagio.append(0)

    #encode
    data_string=json.dumps(cursos[j])
    #Decoded
    decoded = json.loads(data_string)

    infoCursoID.append(str(decoded["id"]))
    infoCursoFullName.append( str(decoded["fullname"]) )

    print("Analizando el curso: "+str(decoded["fullname"]) +" ID:"+str(decoded["id"]))
    id_course=str(decoded["id"])

#obtiene el contenido a detalle de cada curso por id
    contenido = requests.get("http://localhost/moodle/webservice/rest/server.php?wsfunction=core_course_get_contents&wstoken=30401b1161ddb3d0283ae2771d19fdff&moodlewsrestformat=json&courseid="+id_course)
    contenidoCurso.append(contenido.json())
    contenido_string = json.dumps(contenidoCurso[j])
    contenido_decode = json.loads(contenido_string)# Decoded
    for x in range(len(contenido_decode)):
        tam_module = len(contenido_decode[x]["modules"])
        for z in range(tam_module):
            modname = contenido_decode[x]["modules"][z]["modname"]

#si el modulo es visible lo cuenta
            if contenido_decode[x]["modules"][z]["visible"] == 1:
                count_module(j, modname)

            elif modname == "folder" and contenido_decode[x]["modules"][z]["visible"] == 0:
                content = contenido_decode[x]["modules"][z]["contents"]
                folderName = contenido_decode[x]["modules"][z]["name"]
        #lleno las evidencias
                if folderName == "Primer corte"  or folderName == "Segundo corte"  or folderName == "Tercer corte"  :
                    for y in range(len(content)):
                        filename = content[y]["filename"][:len(content[y]["filename"]) - 4]
                        if "-" not in filename:
                            rootEvidences.append(filename)
                        else:
                            evidences.append(filename)
                    verify_evidence(j)

    print("Foros",foros[j])
    print("Tareas", tareas[j])
    print("Folders", folders[j])
    print("Recursos", recursos[j])
    print("Quices", quices[j])
    print("Parciales",parciales[j])
    print("laboratorios", laboratorios[j])
    print("proyectos", proyectos[j])
    print("talleres", talleres[j])
    print("InformePlagio", InformePlagio[j])

def plot_course_results(courses, scores):
    #  create the figure
    fig, ax1 = plt.subplots(figsize=(10, 7))
    pos = np.arange(len(testNames))
    rects = ax1.barh(pos, scores, align='center', height=0.5, color='r', tick_label=testNames)
    ax1.set_title(courses)
    ax1.xaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)
    ax1.set_xlim([0, 20])
    rect_labels = []
    # Lastly, write in the ranking inside each bar to aid in interpretation
    for rect in rects:
        width = int(rect.get_width())
        # The bars aren't wide enough to print the ranking inside
        if (width < 5):
            # Shift the text to the right side of the right edge
            xloc = width + 1
            # Black against white background
            clr = 'black'
            align = 'left'
        else:
            # Shift the text to the left side of the right edge
            xloc = 0.98 * width
            # White on magenta
            clr = 'white'
            align = 'right'
        # Center the text vertically in the bar
        yloc = rect.get_y() + rect.get_height() / 2.0
        label = ax1.text(xloc, yloc, width, horizontalalignment=align,
                         verticalalignment='center', color=clr, weight='bold',
                         clip_on=True)
        rect_labels.append(label)

    # return all of the artists created
    return {'fig': fig,
            'ax': ax1,
            'bars': rects,
            'perc_labels': rect_labels,
            }

def f(IdCurso):
    x=infoCursoID.index(IdCurso)
    courses = infoCursoFullName[x]
    scores = [folders[x], quices[x], tareas[x], foros[x], recursos[x], parciales[x], laboratorios[x], proyectos[x], talleres[x]]
    plot_course_results(courses, scores)
    plt.show()

interact(f,IdCurso=infoCursoID)






