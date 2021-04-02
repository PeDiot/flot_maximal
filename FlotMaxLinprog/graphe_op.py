"""Description.

Graphes pondérés et orientés avec
    - des chaines de caractères pour les noeuds
    - des poids entiers ou flottants.
"""
import re
from typing import Any, Dict, Iterator, List, Tuple, Union
import networkx as nx

Sommet = str
Poids = Union[int, float]
Arrete = Tuple[Sommet, Sommet, Poids]


class GrapheOP:
    """Graphe orienté pondéré.
    
    Exemple :
    
    >>> exemple = GrapheOP.par_str_ordonne('''
    ... A B 4
    ... A C 5
    ... B D 5
    ... C B 2
    ... C D 4
    ... ''')
    >>> exemple
    GrapheOP(voisinage={'A': {'B': 4, 'C': 5}, 'B': {'D': 5}, 'C': {'B': 2, 'D': 4}, 'D': {}})
    >>> print(exemple)
    Problème de flot maximal
    Source : A
    Puit : D
    >>> for sommet in exemple.sommets: print(sommet)
    ...
    A
    B
    C
    D
    >>> for arrete in exemple.arretes: print(arrete)
    ...
    ('A', 'B', 4)
    ('A', 'C', 5)
    ('B', 'D', 5)
    ('C', 'B', 2)
    ('C', 'D', 4)
    >>> exemple["A"]
    {'B': 4, 'C': 5}
    >>> import numpy as np
    >>> np.array(exemple.adjacence)
    array([[0, 4, 5, 0],
           [0, 0, 0, 5],
           [0, 2, 0, 4],
           [0, 0, 0, 0]])
    >>> exemple.est_ordonne
    True
    >>> exemplebis = GrapheOP(
    ... voisinage = {
    'A': {'B': 4, 'C': 5},
    'B': {'D': 5}, 
    'C': {'B': 2, 'D': 4},
    'D': {}
    }
    ... )
    >>> exemplebis == exemple
    True
    >>> exempleter = GrapheOP.par_sommets_arretes(
    ... sommets = ["A", "B", "C", "D"],
    ... arretes = [
    ... ('A', 'B', 4),
    ... ('A', 'C', 5),
    ... ('B', 'D', 5),
    ... ('C', 'B', 2),
    ... ('C', 'D', 4)
    ... ]
    ... )
    >>> exempleter == exemple
    True
    >>> exemple_nx = exemple.convertit_nx_graphe()
    >>> exemple_nx.edges
    OutEdgeView([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'B'), ('C', 'D')])
    >>> exemple_nx.nodes
    NodeView(('A', 'B', 'C', 'D'))
    >>> exemple_nx.adj
    AdjacencyView({'A': {'B': {'capacité': 4}, 'C': {'capacité': 5}}, 'B': {'D': {'capacité': 5}}, 'C':
    {'B': {'capacité': 2}, 'D': {'capacité': 4}}, 'D': {}})
    """
    _motif = re.compile(r"^\s?(\w+)\s(\w+)\s(\d+|\d+.\d+)\s?$")

    def __init__(self, voisinage=Dict[Sommet, Dict[Sommet, Poids]]):
        """Initialise par dictionnaire de voisinage."""
        self._voisinage = voisinage

    def __eq__(self, autre: Any) -> bool:
        """Egalite parfaite pas isomorphisme."""
        if type(self) != type(autre):
            return False
        return self._voisinage == autre._voisinage

    def __repr__(self):
        """Repr pour débug."""
        return f"GrapheOP(voisinage={self._voisinage})"
    
    def __str__(self):
        """Affiche le problème lisiblement."""
        return f"Problème de flot maximal \nSource : {self.sommets[0]} \nPuit : {self.sommets[-1]}" 

    @classmethod
    def par_sommets_arretes(cls, sommets: List[Sommet], arretes: List[Arrete]):
        """Constructeur alternatif par sommets et arretes."""
        voisinage: Dict[Sommet, Dict[Sommet, Poids]] = dict()
        for (depart, arrivee, poids) in arretes:
            if depart not in voisinage:
                voisinage[depart] = {arrivee: poids}
            else:
                if arrivee not in voisinage[depart]:
                    voisinage[depart][arrivee] = poids
                else:
                    raise ValueError(
                        f"L'arrête {depart} {arrivee} est présente deux fois."
                    )

        for sommet in sommets:
            if sommet not in voisinage:
                voisinage[sommet] = dict()

        return cls(voisinage=voisinage)

    @property
    def sommets(self) -> List[Sommet]:
        """Itérateur des sommets."""
        return [ 
            sommet for sommet in self._voisinage.keys()
        ]

    @property
    def arretes(self) -> List[Arrete]:
        """Itère sur les arrêtes."""
        arretes = []
        for sommet, voisins in self._voisinage.items():
            for voisin, poids in voisins.items():
                arretes.append(
                    (sommet, voisin, poids)
                )
        return arretes
    
    @property
    def adjacence(self) -> List[List[Poids]]:
        """Renvoie une matrice d'adjacence."""
        resultat = list()
        for depart in self.sommets:
            ligne = list()
            for arrivee in self.sommets:
                if arrivee in self._voisinage[depart]:
                    ligne.append(self._voisinage[depart][arrivee])
                else:
                    ligne.append(0)
            resultat.append(ligne)
        return resultat
    
    def __getitem__(self, sommet: Sommet) -> Dict[Sommet, Poids]:
        """Renvoit le voisinage du sommet."""
        return self._voisinage[sommet]

    @classmethod
    def par_str_ordonne(cls, graphe: str) -> "GrapheOP":
        """Permet de construire par chaine de caractère."""
        arretes = list()
        for ligne in graphe.strip().splitlines():
            if (resultat := cls._motif.match(ligne)) is not None:
                depart, arrivee, poids = resultat.groups()
            else:
                raise ValueError(
                    f"Il y a un problème sur cette ligne>>\n{ligne}"
                )
            try:
                poids_numerique: Poids = int(poids)
            except ValueError:
                poids_numerique = float(poids)
            arretes.append((depart, arrivee, poids_numerique))
        sommets = list(set([depart for (depart, _, _) in arretes]))
        for _, arrivee, _ in arretes:
            if arrivee not in sommets:
                sommets.append(arrivee)
        return cls.par_sommets_arretes(sommets=sommets, arretes=arretes)

    @property
    def est_ordonne(self) -> bool:
        """Vérifie que la matrice d'adjacence n'est pas symétrique."""
        matrice = self.adjacence
        return matrice != [
            [matrice[j][i] for j, _ in enumerate(ligne)]
            for i, ligne in enumerate(matrice)
        ]
    
    def convertit_nx_graphe(self) -> nx.DiGraph:
        """Transforme le graphe orienté pondéré en un objet networkx."""
        res = nx.DiGraph()
        res.add_weighted_edges_from(
            [
                arrete for arrete in self.arretes
            ],
            weight="capacité"
        )
        return res
