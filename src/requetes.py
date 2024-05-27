#fichier où seront implémenter les requêtes python
import json
import networkx as nx
import itertools
import time
import random


#Q1
def json_ver_nx(chemin:str):
    with open(chemin, mode="r", encoding="utf-8") as file:
        G = nx.Graph()
        for line in file:
            acteurs = json.loads(line)["cast"]
            #print(acteurs)
            acteurs2 = []
            for charac in acteurs:
                acteurs2.append(charac.strip("[]"))
            #for acteur in acteurs2:
            #    for i in acteurs2:
            #       if i != acteur:
            #           G.add_edge(acteur,i)
            #permet de gagner un peu plus de 10s
            G.add_edges_from(itertools.combinations(acteurs2,2))
            
                
        print(len(G.edges))
        print(len(G.nodes))
    return G


        
             

            

            
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
    #print(collaborateurs)
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

def distance_naive(G ,acteur1, acteur2):
    k=0
    while est_proche(G ,acteur1, acteur2,k) is not True:
        k+=1
    return k

def distance(G ,acteur1, acteur2):

    if acteur1 not in G.nodes:
        print(acteur1,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(acteur1)
    distance = 0
    while acteur2 not in collaborateurs:
        distance += 1
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return distance

def distance2(G:nx.Graph,node1:str, node2:str ) -> int:
    try:
        lenght = nx.shortest_path_length(G, node1,node2)
        return lenght
    except nx.NetworkXNoPath:
        return None

#Q4
def centralite(G,u):
    collaborateurs = set()
    collaborateurs.add(u)
    #print(collaborateurs)
    distance = 0
    lenG = len(G.nodes)
    #print(lenG)
    while len(collaborateurs) < lenG:
        #print(distance)
        #print(len(collaborateurs))
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        if collaborateurs_directs == set():
            return distance
        distance += 1
        collaborateurs = collaborateurs.union(collaborateurs_directs)

    return distance

def centralite2(G:nx.Graph,actor:str) -> int:
    distances_paths = set()
    actor_to_check = set(node for node in G.nodes)
    actor_to_check.remove(actor)
    for node in actor_to_check:
        lenght=distance2(G, actor,node)
        if lenght != None :distances_paths.add(lenght)
        # print(f"calculating centralite ==> {actor} to {node} lengh is = {lenght}")
    return max(distances_paths)

def centralite3(G,actor):
    distance = 0
    en_cour = G.adj[actor]
    set_actor_pass = {actor}
    while en_cour != set():
        voisin = set()
        for acteur in en_cour:
            for acteur_v in G.adj[acteur]:
                if acteur_v not in set_actor_pass:
                    voisin.add(acteur_v)
        set_actor_pass = set_actor_pass.union(en_cour)
        en_cour = voisin
        if en_cour == set():
            return distance
        distance += 1
    return distance

def centralite5(G,actor):
    distance = 0
    en_cour = G.adj[actor]
    set_actor_pass = {actor}
    while en_cour != set():
        voisin = set()
        for acteur in en_cour:
            for acteur_v in G.adj[acteur]:
                if acteur_v not in set_actor_pass:
                    voisin.add(acteur_v)
        set_actor_pass = set_actor_pass.union(en_cour)
        old_en_cour = en_cour
        en_cour = voisin
        if en_cour == set():
            return (distance, actor, random.choice(list(old_en_cour)))
        distance += 1
    return (distance, actor, random.choice(list(en_cour)))


def centralite4(G:nx.Graph,actor:str,argument_dict:dict) -> list[dict, int]:
    max_distance:int = 0
    actor_to_check = set(node for node in G.nodes)
    actor_to_check.remove(actor)
    
    for node in actor_to_check:
        keys = [(actor, node), (node, actor)]
        argument_dict_keys =  argument_dict.keys()
        if keys[0] in argument_dict_keys or keys[1] in argument_dict_keys:
            if max_distance < argument_dict[keys[0]]: max_distance = argument_dict[keys[0]]
        else: 
            lenght = distance2(G, actor, node)
            if lenght != None:
                for key in keys:
                    argument_dict[key] = lenght
                if max_distance < lenght: max_distance = argument_dict[keys[0]]
        # print(f"calculating centralite ==> {actor} to {node} lengh is = {lenght}")
    return argument_dict,max_distance





def parcours(G, depart):
    pile = [depart]
    atteint = [depart]
    while (len(pile)>0):
        noeud_courant = pile.pop()
        print(noeud_courant)
        for voisin in G[noeud_courant]:
            if not voisin in atteint:
                pile.append(voisin)
                atteint.append(voisin)
        return atteint



def centre_hollywood(G:nx.Graph) -> str:
    liste_centralite_acteur = []
    for acteur in G.nodes:
        tmp_centralite = (acteur, centralite5(G,acteur)[0])
        liste_centralite_acteur.append(tmp_centralite)
    acteur_centrale = min(liste_centralite_acteur, key=lambda acteur: acteur[1])
    return acteur_centrale[0]

def centre_hollywood3(G):
    random_actor = random.choice(list(G.nodes))
    c1 = centralite5(G, random_actor)
    c2  = centralite5(G, c1[2])
    index = c2[0] // 2
    li_central = set()

    
    collab_fin = collaborateurs_proches(G, c1[2], index+1)
    collab_deb = collaborateurs_proches(G,c2[2], index)
    for acteur in collab_fin:
        if acteur in collab_deb:
            li_central.add(acteur)
    return li_central



    


#Q5
def eloignement_max(G:nx.Graph):
    distance_max = 0
    for acteur in G.nodes:
        c = centralite(G, acteur)
        if c[1] > distance_max:
            distance_max = c[1]
    return distance_max

#Bonus
def centralite_groupe():
    ...

#Juste la pour test au fur et a mesure
if __name__ == "__main__" :
    chemin = "./other/data.txt"
    print("Hello World")
    test = json_ver_nx(chemin)
    
    #print(centralite(test,"Frank Vincent"))
    #t=time.time()
    #print(centralite(test,"Frank Vincent"))
    #print(time.time()-t)
    t=time.time()
    #print(centralite5(test,"Sissy Spacek"))
    #print(centralite(test,"Kristoff St. John"))
    ens_centre_act = centre_hollywood3(test)
    print("a")
    for i in ens_centre_act:
        print(centralite5(test,i))

    
    #result = centralite5(test,"Frank Vincent")
    #print(result)
    # print(distance2(test,"Frank Vincent","Iraj Safavi"))
    print(time.time()-t)
    

    #print(test.nodes)
    #print(test.edges)





    
 
