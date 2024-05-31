#fichier où seront implémenter les requêtes python
#import 
import tkinter as Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
from requetes import *

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

def showActorNearestCollaboratorsK():
    print("Collaborateurs proch K")

def showIfActorNearestCollaboratorK():
    print("Est proche K")

def showActorsDistance():
    print("Distance")

def showActorCentrality():
    print("Centralite")

def showHollywoodCenter():
    print("Centre Hollywood")

def showMaxDistance():
    print("Eloignement Max")

# interface graphique
def leftPanel():
    # relief='sunken'
    sidebar = Frame(root, width=200, bg='#CCC', height=500,borderwidth=2)

    # A compléter
    #Collaborateur Communs
    actorCommonCollabButton = Button(sidebar, text="Collaborateurs Communs", command=showActorsCommonComllaborators)
    actorCommonCollabButton.pack(padx=(20),pady=(20))

    #Collaborateur proche en k
    actorNearCollabKButton = Button(sidebar, text="Collaborateurs Proches en k", command=showIfActorNearestCollaboratorK)
    actorNearCollabKButton.pack(padx=(20),pady=(20))
    
    #Est proche en K
    actorIfNearCollabKButton = Button(sidebar, text="Est Proches en k", command=showActorNearestCollaboratorsK)
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

     # A compléter

    mainarea.pack(expand=True, fill='both', side='right')

def GUI(): #interface graphique utilisateur
    #A finir
    global root
    root = Tk()
    root.geometry('1000x500')
    root.title("The Beacon Finder")
    leftPanel()
    rightPanel()
    root.mainloop()
    return root

def afficheGUI():
    root.mainloop()


if __name__ == "__main__" :
    # Initialisation et lancement
    print("Hello World")
    # print(load_json()) #Pour tester si on arrive bien à récuperer le ficher
    # GRAPH = json_ver_nx(load_json()) #charge un fichier choisi par l'utilisateur et le transforme en Graph Nx
    print(GRAPH)
    afficheGUI(GUI()) #Affiche l'interface graphique

#############################################################
#   LE CODE N EST PAS PROTEGER A TOUS MOMENT IL PEUT CRASH  #
#############################################################
