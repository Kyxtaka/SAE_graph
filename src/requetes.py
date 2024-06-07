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

    Complexité : O(N)
    temps d'éxécution max: environ 0.0006s sur data.txt
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

    Returns:
        Un ensemble contenant les identifiants des collaborateurs proche à k distance
    Complexité : O(N**3)
    temps d'éxécution max: environ 51s sur data.txt avec k=15
    """
   
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs

def est_proche(G ,acteur1, acteur2, k):
    """
    complexité : O(N**3)
    temps d'éxécution max: environ 0.0006s sur data.txt
    """
    collab = collaborateurs_proches(G,acteur1,k)
    if collab != None:
        return acteur2 in collab
    return None

def distance_naive(G ,acteur1, acteur2):
    """
    complexité : O(N**3)
    temps d'éxécution max: ?
    """
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
    Complexité : O(N**3)

    temps d'éxécution max: 28.11741 pour data.txt
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
    """
    Complexité : ?
    temps d'éxécution max: 0.00192s pour data.txt
    """
    try:
        lenght = nx.shortest_path_length(G, node1,node2)
        return lenght
    except nx.NetworkXNoPath:
        return None
    
def distance3(G,node1,node2,d=1):
    """
    complexité : ?
    fonction ne fonctionne pas car ne prend pas en compte les cycle et revient en arrière
    """
    if node1 == node2:
        return 0
    voisin_node1 = G.adj[node1]
    if node2 in voisin_node1:
        return d
    for v in voisin_node1: 
        d = distance3(G,v,node2,d+1) 
    return d
    

#Q4

def centralite(G:nx.Graph,actor:str) -> int:
    """
    complexité : O(N*complexité disatnce2) voir ############################
    temps d'éxécution max:11s avec une centralite de 4 pour data_10000
    """
    distances_paths = set()
    actor_to_check = set(node for node in G.nodes)
    actor_to_check.remove(actor)
    for node in actor_to_check:
        lenght=distance2(G, actor,node)
        if lenght != None :distances_paths.add(lenght)
        # print(f"calculating centralite ==> {actor} to {node} lengh is = {lenght}")
    return max(distances_paths)

def centralite2(G,u):
    """
    complexité : O(N**3)
    temps d'éxécution max: 26s avec centralite de l'acteur à 15 sur data.txt
    """
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



def centralite3(G,actor):
    """
    complexité : O(N**3)
    temps d'éxécution max: 10s avec centralite de l'acteur à 15 sur data.txt
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
        en_cour = voisin
        if en_cour == set():
            return distance
        distance += 1
    return distance


def centralite4(G:nx.Graph,actor:str,argument_dict:dict) -> list[dict, int]:
    """
    complexité : O(N*complexité distance 2 ) ################################
    temps d'éxécution max: ? je comprend pas ce qu'il faut mettre pour le paramètre argument_dict ###########################
    """
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
    """
    complexité : O(N**3)
    temps d'éxécution max: 4.5s avec centralite de l'acteur à 15 sur data.txt
    """
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
    """
    complexité : voir compléxité de nx.single_source_dijkstra_path_length ###############################
    temps d'éxécution max: 10 s avec centralite de l'acteur à 15 sur data.txt
    """
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
               et voisin_aleatoire un acteur aléatoire parmi les derniers voisins visités.
               Retourne None si la distance maximale est atteinte sans exploration complète.

    Complexité O(N**3)
    temps d'éxécution max: 4.5s avec centralite de l'acteur à 15 sur data.txt
    """   
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
        if en_cour == set():
            return (distance, actor, random.choice(list(old_en_cour)))
        if distance == distance_max:
            return None
        
        
    return (distance, actor, random.choice(list(en_cour)))
 


def centre_hollywood(G:nx.Graph) -> str:
    """
    Complexité : ? ################################
    fonctionne pas 
    """
    node_au_pif =  random.choice(list(G.nodes))
    all_node = [node for node in G.nodes]
    c1 = centralite6(G,node_au_pif) #O(N**3)
    c2 = centralite6(G,c1[1]) #O(N**3)
    centrale_index = c2[2]//2
    return all_node[centrale_index], centrale_index 



def centre_hollywood3(G):
    """
    Complexité :  O(N**4)
    temps d'éxecution : 146, temps d'execution change beaucoup en fonction de l'acteur random
    """
    random_actor = random.choice(list(G.nodes)) # va changer de plusieur dizaine de seconde le temps d'execution
    #random_actor="Burt Lancaster"
    c1 = centralite5(G, random_actor) #O(N**3)
    c2  = centralite5(G, c1[2]) #O(N**3)
    index = c2[0] // 2

    ens = set()
    collab_fin = collaborateurs_proches(G, c1[2], index+1) #O(N**3)
    collab_deb = collaborateurs_proches(G,c2[2], index) #O(N**3)
    for acteur in collab_fin:
        if acteur in collab_deb:
            centre_acteur = centralite5(G,acteur) #O(N**3), prend beaucoup de temps car il ya beaucoup de acteur dans collab_deb donc on execute beaucoup de fois centralite5
            ens.add(centre_acteur)
    return min(ens, key=lambda centre_acteur:centre_acteur[0])


def centre_hollywood4(G):
    """
    complexité : O(N**4)
    temps d'éxecution : 19.5s, temps d'execution change de quelque secondes en fonction de l'acteur random
    ne fonctionne pas si l'eloignement max est pair
    """
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


def centre_hollywood5(G):
    """
    Complexité : O(N**6)
    temps d'éxecution: 26s temps d'execution change de quelque secondes en fonction de l'acteur random
    """
    random_actor = random.choice(list(G.nodes))
    
    c = centralite7(G, random_actor)
    c1  = centralite7(G, c[2])
    c2  = centralite7(G, c1[2])


    
    if c2[0] % 2 == 0:
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

    Complexité : O(N**3)
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




def centre_hollywood_distance_max_pair(G, c1, c2):
    """
    Trouve l'acteur central dans un graphe lorsque la distance maximale est paire.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.
        c1 (tuple): Un tuple (distance, acteur, acteur_central) obtenu à partir de la fonction `centralite7`.
        c2 (tuple): Un tuple (distance, acteur, acteur_central) obtenu à partir de la fonction `centralite7`.

    Returns:
        str: L'identifiant de l'acteur central trouvé.

    Complexité : O(N**4)
    """    
    index = c2[0] //2 
    collab_c1_a_index = ens_collab_a_k_distance(G,c1[2],index) #O(N**3)
    collab_c2_a_index = ens_collab_a_k_distance(G,c2[2],index) #O(N**3)

    random_actor = random.choice(list(G.nodes))
    c3 = centralite7(G, random_actor) #O(N**3)
    c4  = centralite7(G, c3[2]) #O(N**3)
    collab_c3_a_index = ens_collab_a_k_distance(G,c3[2],index) #O(N**3)
    collab_c4_a_index = ens_collab_a_k_distance(G,c4[2],index) #O(N**3)

    ens = set()
    for acteur1 in collab_c1_a_index:
        if acteur1 in collab_c2_a_index and acteur1 in collab_c3_a_index and acteur1 in collab_c4_a_index:
            ens.add(acteur1)

    for acteur in ens:#O(N)
        centralite_acteur = centralite7(G,acteur,index) #O(N**3)
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

    Compléxité : O(N**6)
    """    
    index = c2[0] // 2
    ens = set()
    collab_fin = ens_collab_a_k_distance(G,c1[2],index) #O(N**3)
    collab_deb = ens_collab_a_k_distance(G,c2[2],index) #O(N**3)
    for acteur1 in collab_fin:
        for acteur2 in collab_deb:
            if acteur1 != acteur2 and est_proche(G,acteur1,acteur2,1): #O(N**3)
                centre_acteur1 = centralite7(G,acteur1) #O(N**3)
                centre_acteur2 = centralite7(G,acteur2) #O(N**3)
                ens.add(centre_acteur1)
                ens.add(centre_acteur2)
                return min(ens, key=lambda centre_acteur:centre_acteur[0])[1] #O(n)
            

def centre_hollywood6(G):
    """
    Trouve l'acteur central du graphe.

    Args:
        G (networkx.Graph): Le graphe représentant les relations entre les acteurs.

    Returns:
        str: L'identifiant de l'acteur central trouvé par l'algorithme.
    
    Compléxité : O(N**6)
    temps d'éxecution: 26s temps d'execution change de quelque secondes en fonction de l'acteur random
    """   
    random_actor = random.choice(list(G.nodes))
    # calcule de la distance maximale entre deux acteurs
    c = centralite7(G, random_actor) #O(n3)
    c1  = centralite7(G, c[2]) #O(n3)
    c2  = centralite7(G, c1[2]) #O(n3)
    if c2[0] % 2 == 0:
        return centre_hollywood_distance_max_pair(G,c1,c2) #O(N**4)
    else:
        print("a")
        return centre_hollywood_distance_max_impair(G,c1,c2) #O(N**6)
            
    
#Q5
def eloignement_max(G:nx.Graph):
    """
    Complexité : O(N**4)
    """
    distance_max = 0
    for acteur in G.nodes: #O(N)
        c = centralite5(G, acteur) #O(N**3)
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
    
    Complexité : O(N**3)
    """    
    random_actor = random.choice(list(G.nodes))
    c1 = centralite7(G, random_actor)
    c2  = centralite7(G, c1[2])
    return centralite7(G,c2[2])

#Bonus
def centralite_groupe():
    ...

#Juste la pour test au fur et a mesure
if __name__ == "__main__" :
    chemin = "./other/data.txt"
    print("Hello World")
    
    test = json_ver_nx(chemin)
    
    ################### collaborateur_commun

    #t=time.time()
    #print(collaborateurs_communs(test, "Mel Gibson", "Anna May Wong"))
    #print(time.time()-t, "pour collaborateur commun qui renvoie un set()")
    
    
    #t=time.time()
    #print(collaborateurs_communs(test, "Mark Hamill", "Harrison Ford"))
    #print(time.time()-t, "pour collaborateur commun qui à des collaborateur commun")

    ################### collaborateur_proche

    #t=time.time()
    #print(collaborateurs_proches(test, "Mel Gibson", 20))
    #print(time.time()-t, "temps pour collaborateur proche avec k = 15")
    
    ################### distance

    #t=time.time()
    #print(distance(test,"David S. Miller", "Two pupils' fathers"))
    #print(time.time()-t, "temps pour distance avec distance entre les acteurs de 15")

    #t=time.time()
    #print(distance2(test,"David S. Miller", "Two pupils' fathers"))
    #print(time.time()-t, "temps pour distance2 avec distance entre les acteurs de 15")

    ################### centralite
    
    #t=time.time()
    #print(centralite(test,'Veriano Genesi'))
    #print(time.time()-t, "temps pour centralite avec centralite à 4 sur data_10000.txt")

    #t=time.time()
    #print(centralite2(test,"Two pupils' fathers"))
    #print(time.time()-t, "temps pour centralite2 avec centralite à 15")
    
    #t=time.time()
    #print(centralite3(test,"Two pupils' fathers"))
    #print(time.time()-t, "temps pour centralite3 avec centralite à 15")

    #t=time.time()
    #print(centralite4(test,"Two pupils' fathers"))
    #print(time.time()-t, "temps pour centralite4 avec centralite à 15")

    #t=time.time()
    #print(centralite5(test,"Two pupils' fathers"))
    #print(time.time()-t, "temps pour centralite5 avec centralite à 15")

    #t=time.time()
    #print(centralite6(test,"Two pupils' fathers"))
    #print(time.time()-t, "temps pour centralite6 avec centralite à 15")

    #t=time.time()
    #print(centralite7(test,"Two pupils' fathers"))
    #print(time.time()-t, "temps pour centralite7 avec centralite à 15")

    ################### centre_hollywood

    #t=time.time()
    #print(centre_hollywood3(test))
    #print(time.time()-t, "temps pour centre_hollywood3")

    #t=time.time()
    #print(centre_hollywood4(test))
    #print(time.time()-t, "temps pour centre_hollywood4")

    #t=time.time()
    #print(centre_hollywood5(test))
    #print(time.time()-t, "temps pour centre_hollywood5")

    #t=time.time()
    #print(centre_hollywood6(test))
    #print(time.time()-t, "temps pour centre_hollywood6")

    ################### eloignement_max
    
    t=time.time()
    print(eloignement_max(test))
    print(time.time()-t, "temps pour eloignement_max")

    t=time.time()
    print(eloignement_max3(test))
    print(time.time()-t, "temps pour eloignement_max")
    
    #print(eloignement_max3(test))
    
    ########distance_naive, centralite
    
 
