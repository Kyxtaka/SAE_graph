#fichier où seront implémenter les requêtes python
import json
import networkx as nx
import typing

#Q1
def json_ver_nx(chemin:str) -> dict:
    with open(chemin, mode="r", encoding="utf-8") as file:
        file_dict = json.loads(file.read())
        print(file_dict)
        

#Q2
def collaborateurs_communs():
    ...

#Q3 
def collaborateurs_proches():
    ...

def est_proche():
    ...

def distance_naive():
    ...

def distance():
    ...

#Q4
def centralite():
    ...

def centre_hollywood():
    ...

#Q5
def eloignement_max():
    ...

#Bonus
def centralite_groupe():
    ...

#Juste la pour test au fur et a mesure
if __name__ == "__main__" :
    chemin = "./other/data.txt"
    print("Hello World")
    json_ver_nx(chemin)