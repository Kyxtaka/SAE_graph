#fichier où seront implémenter les requêtes python
#import 
import json
import tkinter as Tk
from tkinter.filedialog import askopenfilename
from tkinter import *

#constant
default_path = "./other/data.txt"
#function
def load_json(dafault = default_path):
    path = askopenfilename()
    print(len(path))
    if len(path) != 0: return path
    return dafault

# interface graphique
def leftPanel(root:Tk):
    # relief='sunken'
    sidebar = Frame(root, width=200, bg='#CCC', height=500,borderwidth=2)


    sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

def GUI(): #interface graphique utilisateur
    root = Tk()
    root.geometry('1000x500')
    root.title("The Beacon Finder")
    mainarea = Frame(root, bg='white', width=500, height=500)
    mainarea.pack(expand=True, fill='both', side='right')
    leftPanel(root)
    root.mainloop()
    return root

def afficheGUI(root:Tk):
    root.mainloop()


if __name__ == "__main__" :
    # Initialisation et lancement
    print("Hello World")
    print(load_json())
    afficheGUI(GUI())