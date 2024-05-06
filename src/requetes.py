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
def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs

def est_proche(G ,acteur1, acteur2, k):
    collab = collaborateurs_proches(G,acteur1,k)
    if collab != None:
        return acteur2 in collab
    return None

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
    chemin = "/home/pierre/Ecole/Ecole/iut/SAE/SAE_graph/SAE_graph/other/data.txt"
    print("Hello World")
    test = json_ver_nx(chemin)
    #print(test.nodes)
    collaborateurs_communs(test,"Sophie Marceau","Filipe Ferrer")
