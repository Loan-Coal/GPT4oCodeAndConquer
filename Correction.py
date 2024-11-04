from collections import deque


def trouver_groupes_chemins(matrice):

    #Initialiser toutes les variables
    lignes = len(matrice)
    colonnes = len(matrice[0])
    visites = [[False for i in range(colonnes)] for i in range(lignes)]
    groupes = []

    #oui je sais sais, pas très propre fonction dans une fonction mais tant pis
    def bfs(ligne, colonne):
        file = deque([(ligne, colonne)])
        groupe = [(ligne, colonne)]
        visites[ligne][colonne] = True

        #c'est comme [i+1][j] ects mais sans avoir à répéter(cool astuce)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        #Parcourir tous les voisins d'un noeud, puis les voisins des voisins 
        while file:
            ligne_actuelle, colonne_actuelle = file.popleft()
            for dl, dc in directions:
                nouvelle_ligne, nouvelle_colonne = ligne_actuelle + dl, colonne_actuelle + dc
                if (0 <= nouvelle_ligne < lignes and 0 <= nouvelle_colonne < colonnes and matrice[nouvelle_ligne][nouvelle_colonne] == 0 and not visites[nouvelle_ligne][nouvelle_colonne]):
                    visites[nouvelle_ligne][nouvelle_colonne] = True
                    groupe.append((nouvelle_ligne, nouvelle_colonne))
                    file.append((nouvelle_ligne, nouvelle_colonne))
        return groupe

    for i in range(lignes):
        for j in range(colonnes):
            if matrice[i][j] == 0 and not visites[i][j]:
                groupes.append(bfs(i, j))

    return groupes

from collections import deque

def calculer_chemin_minimal(matrice, groupe1, groupe2):
    nombre_lignes = len(matrice)
    nombre_colonnes = len(matrice[0])

    # Initialiser la file avec les cases du premier groupe et un chemin vide
    file = deque()
    for (ligne, colonne) in groupe1:
        file.append((ligne, colonne, []))

    # Directions pour se déplacer : haut, bas, gauche, droite
    directions_deplacement = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Tableau pour garder la trace des cases déjà visitées
    cases_visitees = [[False for i in range(nombre_colonnes)] for i in range(nombre_lignes)]

    # Parcourir la file jusqu'à ce qu'on trouve un chemin vers le groupe2
    while file:
        ligne_actuelle, colonne_actuelle, chemin_actuel = file.popleft()

        # Essayer chaque direction pour trouver les voisins
        for deplacement_ligne, deplacement_colonne in directions_deplacement:
            nouvelle_ligne = ligne_actuelle + deplacement_ligne
            nouvelle_colonne = colonne_actuelle + deplacement_colonne

            # Vérifier si la nouvelle position est dans les limites de la matrice et non visitée
            if 0 <= nouvelle_ligne < nombre_lignes and 0 <= nouvelle_colonne < nombre_colonnes:
                if not cases_visitees[nouvelle_ligne][nouvelle_colonne]:
                    cases_visitees[nouvelle_ligne][nouvelle_colonne] = True

                    # Vérifier si la case fait partie du groupe2
                    if (nouvelle_ligne, nouvelle_colonne) in groupe2:
                        return chemin_actuel + [(nouvelle_ligne, nouvelle_colonne)]
                    
                    # Si la case est un obstacle (1), continuer à l'explorer
                    elif matrice[nouvelle_ligne][nouvelle_colonne] == 1:
                        nouveau_chemin = chemin_actuel + [(nouvelle_ligne, nouvelle_colonne)]
                        file.append((nouvelle_ligne, nouvelle_colonne, nouveau_chemin))
                    
    #si aucun chemin n'est trouvé, retourner un chemin vide
    return []

def relier_groupes(matrice, groupes):
    #tant qu'il y a plus d'un groupe, on essaie de les relier
    while len(groupes) > 1:
        liste_distances = []
        
        #parcourir chaque paire de groupes pour trouver le chemin minimal
        for index_premier_groupe, premier_groupe in enumerate(groupes):
            for index_deuxieme_groupe, deuxieme_groupe in enumerate(groupes):
                if index_premier_groupe != index_deuxieme_groupe:
                    chemin_minimal = calculer_chemin_minimal(matrice, premier_groupe, deuxieme_groupe)
                    if chemin_minimal:
                        #stocker la longueur du chemin, les indices des groupes, et le chemin lui-même
                        liste_distances.append((len(chemin_minimal), index_premier_groupe, index_deuxieme_groupe, chemin_minimal))

        #trier les chemins par leur longueur pour trouver le plus court
        liste_distances.sort()
        
        # S'il n'y a pas de chemins, arrêter
        if not liste_distances:
            break

        #prendre le chemin le plus court et relier les deux groupes
        _, indice_groupe1, indice_groupe2, chemin_court = liste_distances[0]

        #remplacer les cases du chemin court par des chemins (0)
        for (ligne, colonne) in chemin_court:
            matrice[ligne][colonne] = 0

        #fusionner les groupes relié dans la liste des groupes
        groupe1 = groupes[indice_groupe1]
        groupe2 = groupes[indice_groupe2]
        groupes[indice_groupe1] = groupe1 + groupe2
        groupes.pop(indice_groupe2)

    #retourner la matrice corrigé avec tous les groupes reliés
    return matrice


#effectuer toutes les fonctions précédente 
def correction(matrice):
    groupes = trouver_groupes_chemins(matrice)
    matrice_corrigee = relier_groupes(matrice, groupes)
    return matrice_corrigee