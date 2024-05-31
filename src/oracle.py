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
    ...

def showActorNearestCollaboratorsK():
    ...

def showIfActorNearestCollaboratorK():
    ...

def showActorsDistance():
    ...

def showActorCentrality():
    ...

def showHollywoodCenter():
    ...

def showMaxDistance():
    ...

# interface graphique
def leftPanel(root:Tk):
    # relief='sunken'
    sidebar = Frame(root, width=200, bg='#CCC', height=500,borderwidth=2)

    # A compléter

    sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

def rightPanel(root:Tk):
    mainarea = Frame(root, bg='white', width=500, height=500)

     # A compléter

    mainarea.pack(expand=True, fill='both', side='right')

def GUI(): #interface graphique utilisateur
    #A finir
    root = Tk()
    root.geometry('1000x500')
    root.title("The Beacon Finder")
    leftPanel(root)
    rightPanel(root)
    root.mainloop()
    return root

def afficheGUI(root:Tk):
    root.mainloop()


if __name__ == "__main__" :
    # Initialisation et lancement
    print("Hello World")
    print(load_json()) #Pour tester si on arrive bien à récuperer le ficher
    GRAPH = json_ver_nx(load_json()) #charge un fichier choisi par l'utilisateur et le transforme en Graph Nx
    afficheGUI(GUI()) #Affiche l'interface graphique

#############################################################
#   LE CODE N EST PAS PROTEGER A TOUS MOMENT IL PEUT CRASH  #
#############################################################