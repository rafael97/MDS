import  requests
import simplejson as json
folders=[]
tareas=[]
foros=[]
recursos=[]
quices=[]

#obtener cursos
r = requests.get("http://localhost/moodle/webservice/rest/server.php?wsfunction=core_course_get_courses&wstoken=30401b1161ddb3d0283ae2771d19fdff&moodlewsrestformat=json")
cursos=[]
contenido_curso=[]
for x in range(1,len(r.json())):
    cursos.append(r.json()[x])
#cursos
for j in range(len(cursos)):
    folders.append(0)
    tareas.append(0)
    foros.append(0)
    recursos.append(0)
    quices.append(0)
    #encode
    data_string=json.dumps(cursos[j])
    #Decoded
    decoded = json.loads(data_string)
    print("Analizando el curso: "+str(decoded["fullname"]) +" ID:"+str(decoded["id"]))
    id_course=str(decoded["id"])
    contenido = requests.get("http://localhost/moodle/webservice/rest/server.php?wsfunction=core_course_get_contents&wstoken=30401b1161ddb3d0283ae2771d19fdff&moodlewsrestformat=json&courseid="+id_course)
    contenido_curso.append(contenido.json())
    contenido_string = json.dumps(contenido_curso[j])
    contenido_decode = json.loads(contenido_string)# Decoded
    for x in range(len(contenido_decode)):
        tam_module = len(contenido_decode[x]["modules"])
        for z in range(tam_module):
            modname = contenido_decode[x]["modules"][z]["modname"]
            #print(modname)
            if modname=="forum":
                foros[j]=foros[j]+1
            if modname == "assign":
                tareas[j] = tareas[j] + 1
            if modname == "folder":
                folders[j] = folders[j] + 1
            if modname == "resource" or modname == "url" or modname == "label" or modname == "page":
                recursos[j] = recursos[j] + 1
            if modname == "quiz":
                quices[j] = quices[j] + 1

    print("Foros",foros[j])
    print("Tareas", tareas[j])
    print("Folders", folders[j])
    print("Recursos", recursos[j])
    print("Quices", quices[j])

"""
Analizando el curso: curso 2 ID:3
Foros 1
Tareas 1
Folders 1
Recursos 2
Quices 1
Analizando el curso: curso 1 ID:4
Foros 2
Tareas 1
Folders 1
Recursos 2
Quices 0
Analizando el curso: curso 3 ID:5
Foros 1
Tareas 1
Folders 1
Recursos 2
Quices 0
Analizando el curso: curso 4 ID:6
Foros 2
Tareas 1
Folders 1
Recursos 1
Quices 0
"""


