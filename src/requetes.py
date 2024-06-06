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
    """
    Trouve les collaborateurs communs entre deux acteurs dans un graphe.
    Args:
        graph (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        acteur1 (str): Le nom du premier acteur.
        acteur2 (str): Le nom du deuxième acteur.

    Returns:
        set: Un ensemble contenant les identifiants des collaborateurs communs entre acteur1 et acteur2.
    """   
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
    """"
    Calcule la distance minimale entre deux acteurs dans un graphe.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        acteur1 (str): Le nom du premier acteur.
        acteur2 (str): Le nom du deuxième acteur.

    Returns:
        int: La distance minimale entre acteur1 et acteur2, ou None si acteur1 ou acteur2 n'existe pas dans le graphe.
    """    
    if acteur1 not in G.nodes:
        print(acteur1,"est un illustre inconnu")
        return None
    if acteur2 not in G.nodes:
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
    
def distance3(G,node1,node2,d=1):
    if node1 == node2:
        return 0
    voisin_node1 = G.adj[node1]
    if node2 in voisin_node1:
        return d
    for v in voisin_node1:
        d = distance3(G,v,node2,d+1)
    return d
    

#Q4
def centralite(G,u):
    
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
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

    
def centralite5(G,actor):
    if actor not in G:
        return None
    distance = 0
    en_cour = G.adj[actor]
    set_actor_pass = {actor}
    while en_cour != set():
        voisin = set()
        distance += 1
        set_actor_pass = set_actor_pass.union(en_cour)
        for acteur in en_cour:
            for acteur_v in G.adj[acteur]:
                if acteur_v not in set_actor_pass:
                    voisin.add(acteur_v)
        old_en_cour = en_cour
        en_cour = voisin      
    return (distance, actor, random.choice(list(old_en_cour)))


def centralite6(G:nx.Graph,actor:str) -> list[str,str,int]:
    # test = nx.single_source_dijkstra_path(G, actor)
    test2 = nx.single_source_dijkstra_path_length(G, actor)
    # test =  nx.single_source_dijkstra(G,actor) 
    max_distance = max(test2.values())
    res = list()
    for key in test2.keys():
        if test2[key] == max_distance: res.append(key)
    return (actor, res[-1], max_distance)

def centralite7(G,actor,distance_max=None):
    """
    Calcule la centralité d'un acteur dans un graphe.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        actor (str): Le nom de l'acteur central.
        distance_max (int, optional): La distance maximale à explorer. Si None, explore jusqu'à épuisement des voisins. Defaults to None.

    Returns:
        tuple: Un tuple (distance, actor, voisin_aleatoire) où distance est la distance finale atteinte, actor est l'acteur d'origine,
               et un acteur aléatoire parmi les derniers voisins visités.
               Retourne None si la distance maximale est atteinte sans exploration complète.
    """   
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
        if distance == distance_max:
            return None
        distance += 1
        
    return (distance, actor, random.choice(list(en_cour)))



def centre_hollywood(G:nx.Graph) -> str:
    node_au_pif =  "Al Pacino"
    all_node = [node for node in G.nodes]
    c1 = centralite6(G,node_au_pif)
    c2 = centralite6(G,c1[1])
    centrale_index = c2[2]//2
    return all_node[centrale_index], centrale_index



def centre_hollywood3(G):
    #random_actor = random.choice(list(G.nodes))
    random_actor="Burt Lancaster"
    c1 = centralite5(G, random_actor)
    c2  = centralite5(G, c1[2])
    index = c2[0] // 2

    ens = set()
    collab_fin = collaborateurs_proches(G, c1[2], index+1)
    collab_deb = collaborateurs_proches(G,c2[2], index)
    for acteur in collab_fin:
        if acteur in collab_deb:
            centre_acteur = centralite5(G,acteur)
            ens.add(centre_acteur)
    print(len(ens))
    return min(ens, key=lambda centre_acteur:centre_acteur[0])



def centre_hollywood4(G):
    random_actor = random.choice(list(G.nodes))
    c1 = centralite5(G, random_actor)
    c2  = centralite5(G, c1[2])
    index = c2[0] // 2

    ens = set()
    collab_fin = collaborateurs_proches(G, c1[2], index)
    collab_deb = collaborateurs_proches(G,c2[2], index)
    for acteur1 in collab_fin:
        for acteur2 in collab_deb:
            if est_proche(G,acteur1,acteur2,1):
                centre_acteur1 = centralite5(G,acteur1)
                centre_acteur2 = centralite5(G,acteur2)
                ens.add(centre_acteur1)
                ens.add(centre_acteur2)
                return min(ens, key=lambda centre_acteur:centre_acteur[0])[1]

def ens_collab_a_k_distance(G,u,k):
    """
    Trouve l'ensemble des collaborateurs situés à une distance k d'un acteur donné dans un graphe.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        u (str): Le nom de l'acteur de départ.
        k (int): La distance à laquelle rechercher les collaborateurs.

    Returns:
        set: Un ensemble contenant les identifiants des collaborateurs situés à une distance k de u,
             ou None si l'acteur u n'existe pas dans le graphe.
    """  
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs_directs = set()
    collaborateurs.add(u)
    #print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs_directs

def centre_hollywood5(G):
    random_actor = random.choice(list(G.nodes))
    
    c = centralite7(G, random_actor)
    c1  = centralite7(G, c[2])
    c2  = centralite7(G, c1[2])


    eloignemnt = eloignement_max3(G)
    if eloignemnt % 2 == 0:
        index = c2[0] //2 
        collab_c1_a_index = ens_collab_a_k_distance(G,c1[2],index)
        collab_c2_a_index = ens_collab_a_k_distance(G,c2[2],index)
        ens = set()
        for acteur1 in collab_c1_a_index:
            for acteur2 in  collab_c2_a_index:
                if acteur1 == acteur2:
                    ens.add(acteur2)
        #return len(ens)
        for acteur in ens:
            centralite_acteur = centralite7(G,acteur,index)
            if centralite_acteur != None:
                return acteur
        
        
    else:
        print("b")
        index = eloignemnt // 2
        ens = set()
        collab_fin = collaborateurs_proches(G, c1[2], index)
        collab_deb = collaborateurs_proches(G,c2[2], index)
        for acteur1 in collab_fin:
            for acteur2 in collab_deb:
                if est_proche(G,acteur1,acteur2,1):
                    centre_acteur1 = centralite5(G,acteur1)
                    centre_acteur2 = centralite5(G,acteur2)
                    ens.add(centre_acteur1)
                    ens.add(centre_acteur2)
                    return min(ens, key=lambda centre_acteur:centre_acteur[0])[1]


def centre_hollywood_distance_max_pair(G, c1, c2):
    """
    Trouve l'acteur central dans un graphe lorsque la distance maximale est paire.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        c1 (tuple): Un tuple (distance, acteur, acteur_central) obtenu à partir de la fonction `centralite7`.
        c2 (tuple): Un tuple (distance, acteur, acteur_central) obtenu à partir de la fonction `centralite7`.

    Returns:
        str: L'identifiant de l'acteur central trouvé.
    """    
    index = c2[0] //2 
    collab_c1_a_index = ens_collab_a_k_distance(G,c1[2],index)
    collab_c2_a_index = ens_collab_a_k_distance(G,c2[2],index)

    random_actor = random.choice(list(G.nodes))
    c3 = centralite7(G, random_actor)
    c4  = centralite7(G, c3[2])
    collab_c3_a_index = ens_collab_a_k_distance(G,c3[2],index)
    collab_c4_a_index = ens_collab_a_k_distance(G,c4[2],index)

    ens = set()
    for acteur1 in collab_c1_a_index:
        if acteur1 in collab_c2_a_index and acteur1 in collab_c3_a_index and acteur1 in collab_c4_a_index:
            ens.add(acteur1)

    for acteur in ens:
        centralite_acteur = centralite7(G,acteur,index)
        if centralite_acteur != None:
            return acteur


def centre_hollywood_distance_max_impair(G, c1, c2):
    """
    Trouve l'acteur central dans un graphe lorsque la distance maximale est impaire.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        c1 (tuple): Un tuple (distance, acteur, acteur_central) obtenu à partir de la fonction `centralite7`.
        c2 (tuple): Un tuple (distance, acteur, acteur_central) obtenu à partir de la fonction `centralite7`.

    Returns:
        str: L'identifiant de l'acteur central trouvé.
    """    
    index = c2[0] // 2
    ens = set()
    collab_fin = ens_collab_a_k_distance(G,c1[2],index)
    collab_deb = ens_collab_a_k_distance(G,c2[2],index)
    for acteur1 in collab_fin:
        for acteur2 in collab_deb:
            if acteur1 != acteur2 and est_proche(G,acteur1,acteur2,1):
                centre_acteur1 = centralite7(G,acteur1)
                centre_acteur2 = centralite7(G,acteur2)
                ens.add(centre_acteur1)
                ens.add(centre_acteur2)
                return min(ens, key=lambda centre_acteur:centre_acteur[0])[1]
            

def centre_hollywood6(G):
    """
    Trouve l'acteur central du graphe.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.

    Returns:
        str: L'identifiant de l'acteur central trouvé par l'algorithme.
    """   
    random_actor = random.choice(list(G.nodes))
    # calcule de la distance maximale entre deux acteurs
    c = centralite7(G, random_actor)
    c1  = centralite7(G, c[2])
    c2  = centralite7(G, c1[2])
    if c2[0] % 2 == 0:
        return centre_hollywood_distance_max_pair(G,c1,c2)
    else:
        print("a")
        return centre_hollywood_distance_max_impair(G,c1,c2)
            
    
#Q5
def eloignement_max(G:nx.Graph):
    distance_max = 0
    for acteur in G.nodes:
        c = centralite(G, acteur)
        if c > distance_max:
            distance_max = c
    return distance_max


def eloignement_max3(G):
    """
    Calcule l'éloignement maximal d'un graphe.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.

    Returns:
        int: La distance maximale obtenue après une série de calculs de centralité.
    """    
    random_actor = random.choice(list(G.nodes))
    c1 = centralite5(G, random_actor)
    c2  = centralite5(G, c1[2])
    return centralite5(G,c2[2])[0]

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
    #print(centre_hollywood5(test))
    """liste5 = []
    liste6 = []
    i = 0
    while i < 100:
        liste5.append(centre_hollywood5(test))
        liste6.append(centre_hollywood6(test))
        i+=1
    moyenne5 = sum(liste5)/len(liste5)
    moyenne6 = sum(liste6)/len(liste6)
    print(moyenne5, moyenne6)
    """



    t=time.time()
    a = centre_hollywood6(test)
    print(time.time()-t)
    print(a)
    print(centralite7(test,a))
    

    
 
