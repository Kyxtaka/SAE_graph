#fichier où seront implémenter les requêtes python
import json
import networkx as nx
import typing

#Q1
def json_ver_nx(chemin:str) -> nx.Graph:
    json_file = []
    with open(chemin, mode="r", encoding="utf-8") as file:
        for line in file:
            json_file.append(json.loads(line))
    actors_list = set()
    actors_edges = set()
    for film in json_file:
        tmp_actors = film['cast']
        for i in range(len(tmp_actors)):
            for k in range(i+1,len(tmp_actors)):
                actorName_1 = str(tmp_actors[i])
                actorname_2 = str(tmp_actors[k])
                actorName_1 = actorName_1.translate({ord(i): None for i in "[]'"})
                actorname_2 = actorname_2.translate({ord(i): None for i in "[]'"})
                actors_list.add(actorName_1)
                actors_edges.add((actorName_1,actorname_2))
    # print(actors_edges)
    # print(len(actors))
    print(len(actors_edges))
    Graph = nx.Graph()
    Graph.add_edges_from(actors_edges)
    print(len(Graph.nodes))
    return Graph
#Q2
def collaborateurs_communs(graph, acteur1, acteur2):
    ens_commun = set()
    for collab in graph.adj[acteur1]:
        if collab in graph.adj[acteur2]:
            ens_commun.add(collab)
    return ens_commun

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
def centralite(G:nx.Graph, u) -> int:
    liste_distance = []
    for acteur in G.nodes:
        liste_distance.append(distance(G,u,acteur))
    return max(liste_distance)

def centre_hollywood(G:nx.Graph) -> str:
    liste_centralite_acteur = []
    for acteur in G.nodes:
        tmp_centralite = tuple(acteur, centralite(G,acteur))
        liste_centralite_acteur.append(tmp_centralite)
    acteur_centrale = min(liste_centralite_acteur, key=lambda acteur: acteur[1])
    return acteur_centrale[0]
    
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
    test = json_ver_nx(chemin)
    #print(test.nodes)
    collaborateurs_communs(test,"Sophie Marceau","Filipe Ferrer")
