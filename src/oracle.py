#fichier où seront implémenter les requêtes python
#import 
import tkinter as Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
from requetes import *
from tkinter import simpledialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

#constant
default_path = "./other/data.txt"
GRAPH = None

#function
def load_json(dafault = default_path):
    path = askopenfilename()
    print(len(path))
    if len(path) != 0: return path
    return dafault

def nxGraphInit(pathRoute):
    GRAPH = json_ver_nx(pathRoute)
    return GRAPH

def getTextEntryInput(textField:Entry) -> str:
    return textField.get()

#Implementation des requetes en affichage graphique (GUI)
#Toutes les les requtes se verront affichier une boites de dialogue affichant la réponse a sa fonction
def showActorsCommonComllaborators(): #doit affichier une fentre de dialogue
    print("Collaborateurs Commun")
    actor1Entry = simpledialog.askstring("Acteur 1","Donner le nom du premier acteur")
    actor2Entry = simpledialog.askstring("Acteur 2","Donner le nom du deuxieme acteur")
    actorCommonCollabData = collaborateurs_communs(GRAPH,actor1Entry,actor2Entry)
    messagebox.showinfo("Collaborateur Communs",f"Les collaborateurs commun de '{actor1Entry}' et de '{actor2Entry}' sont : {actorCommonCollabData}.")


def showActorNearestCollaboratorsK():
    print("Collaborateurs proches K")
    actorEntry = simpledialog.askstring("Acteur depart","Donner le nom de l'acteur de depart")
    kIndex = simpledialog.askinteger("nombre de sauts","A combien de k pres")
    actorNearCollabData = collaborateurs_proches(GRAPH,actorEntry,kIndex)
    messagebox.showinfo("Collaborateur Porche",f"Les collaborateurs proches de '{actorEntry}' sont : {actorNearCollabData}.")

def showIfActorNearestCollaboratorK():
    print("Est proche a K pres")
    actor1Entry = simpledialog.askstring("Acteur recherche","Donner le nom de l'acteur recherche")
    actor2Entry = simpledialog.askstring("Acteur depart","Donner le nom de l'acteur de depart")
    kIndex = simpledialog.askinteger("nombre de sauts","A combien de k pres")
    isProche = est_proche(GRAPH, actor2Entry,actor1Entry,kIndex)
    if isProche: messagebox.showinfo("Acteur Proche",f"L'acteur '{actor1Entry}' est bien un collaborateur proche de '{actor2Entry}'.")
    else: messagebox.showinfo("Acteur Proche",f"L'acteur '{actor1Entry}' n'est pas un collaborateur proche de '{actor2Entry}'.")

def showActorsDistance():
    print("Distance")
    actor1Entry = simpledialog.askstring("Nom acteur 1","Donner le nom du premier acteur")
    actor2Entry = simpledialog.askstring("Nom acteur 2","Donner le nom du deuxieme acteur")
    actorsDistanceData = distance2(GRAPH,actor1Entry,actor2Entry)
    messagebox.showinfo("Distance",f"La distance qui separe l'acteur '{actor1Entry}' de l'acteur '{actor2Entry}' est de {actorsDistanceData}.")

def showActorCentrality():
    print("Centralite")
    actorEntry = simpledialog.askstring("Nom acteur","Donner le nom d'un acteur")
    actorCentrality = centralite5(GRAPH, actorEntry)
    messagebox.showinfo("Centralite",f"La centralite de l'acteur '{actorEntry}' est de {actorCentrality[0]}.")

def showHollywoodCenter():
    print("Centre Hollywood")
    hollywoodCenterData = centre_hollywood4(GRAPH)
    messagebox.showinfo("Centre Hollywood",f"L'acteur ce trouvent au centre est : {hollywoodCenterData}.")

def showMaxDistance():
    print("Eloignement Max")
    maxDistanceData = eloignement_max3(GRAPH)
    messagebox.showinfo("Eloignement Max",f"La plus grande distance qui separe deux acteur est de {maxDistanceData}.")
    
# interface graphique
def leftPanel():
    # relief='sunken'
    sidebar = Frame(root, width=200, bg='#CCC', height=500,borderwidth=2)

    # A compléter
    #Collaborateur Communs
    actorCommonCollabButton = Button(sidebar, text="Collaborateurs Communs", command=showActorsCommonComllaborators)
    actorCommonCollabButton.pack(padx=(20),pady=(20))

    #Collaborateur proche en k
    actorNearCollabKButton = Button(sidebar, text="Collaborateurs Proches en k", command=showActorNearestCollaboratorsK)
    actorNearCollabKButton.pack(padx=(20),pady=(20))
    
    #Est proche en K
    actorIfNearCollabKButton = Button(sidebar, text="Est Proches en k", command=showIfActorNearestCollaboratorK)
    actorIfNearCollabKButton.pack(padx=(20),pady=(20))

    #Distance entre deux acteurs
    actorDistanceButton = Button(sidebar, text="Distance entre 2 Acteurs", command=showActorsDistance)
    actorDistanceButton.pack(padx=(20),pady=(20))

    #Centralite d'un acteur
    actorCentralityButton = Button(sidebar, text="Centralite Acteur", command=showActorCentrality)
    actorCentralityButton.pack(padx=(20),pady=(20))

    #Centre Hollywood
    actorCentreHollwoodButton = Button(sidebar, text="Centre Hollywood", command=showHollywoodCenter)
    actorCentreHollwoodButton.pack(padx=(20),pady=(20))

    #Eloignement Max
    eloignementMaxButton = Button(sidebar, text="Eloignement Max", command=showMaxDistance)
    eloignementMaxButton.pack(padx=(20),pady=(20))

    sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

def rightPanel():
    mainarea = Frame(root, bg='white', width=500, height=500)
    fig = Figure()
    a = fig.add_subplot(111)
    pos = nx.spring_layout(GRAPH)
    nx.draw(GRAPH, pos, with_labels=True,ax=a)
    canvas = FigureCanvasTkAgg(fig, master = mainarea)
    canvas.draw() 
    canvas.get_tk_widget().pack(side="right", fill="both", expand=1) 
    mainarea.pack(expand=True, fill='both', side='right')

def GUI(): #interface graphique utilisateur
    #A finir
    global root
    root = Tk()
    root.geometry('1000x500')
    root.title("The Beacon Finder")
    leftPanel()
    #rightPanel()
    root.mainloop()
    return root

def afficheGUI():
    root.mainloop()


if __name__ == "__main__" :
    # Initialisation et lancement
    print("Hello World")
    # print(load_json()) #Pour tester si on arrive bien à récuperer le ficher
    GRAPH = json_ver_nx(load_json()) #charge un fichier choisi par l'utilisateur et le transforme en Graph Nx
    print(GRAPH)
    GUI()
    afficheGUI() #Affiche l'interface graphique

#############################################################
#   LE CODE N EST PAS PROTEGER A TOUS MOMENT IL PEUT CRASH  #
#############################################################
################################################################
#   CODE FINI A 90% MANQUE PLUS QU A FAIRE QUELQUE PROTECTION  #
################################################################