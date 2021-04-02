"""Description.

Module pour la résolution du problème de flot maximal à l'aide de l'algorithme de programmation linéaire HiGHS.

Exemple: 

>>> exemple = GrapheOP.par_str_ordonne('''
...  A B 4
...  A C 5
...  B D 5
...  C B 2
...  C D 4
...  ''')
>>> linprog_exemple = LinprogGraph(exemple)
>>> linprog_exemple.affiche_solution()
Problème de flot maximal
Source : A
Puit : D
┌────────┬─────────┬──────────────┐
│ Départ │ Arrivée │ Flot maximal │
├────────┼─────────┼──────────────┤
│ A      │ B       │ 4.0          │
│ A      │ C       │ 5.0          │
│ B      │ D       │ 5.0          │
│ C      │ B       │ 1.0          │
│ C      │ D       │ 4.0          │
└────────┴─────────┴──────────────┘

"""

from .graphe_op import (
    GrapheOP,
    Sommet,
    Arrete,
    Poids
)
from scipy.optimize import linprog
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
from rich.table import Table

class LinprogGraph:
    """Classe de résolution du problème de flot maximal.
    
    Exemple :
    
    >>> linprog_exemple._objectif()
    array([-1,  0,  0,  0,  0,  0,  0])
    >>> linprog_exemple._calcule_A_ub()
    array([[-1,  0,  0,  0,  0,  0,  0],
           [ 0, -1,  0,  0,  0,  0,  0],
           [ 0,  0, -1,  0,  0,  0,  0],
           [ 0,  0,  0, -1,  0,  0,  0],
           [ 0,  0,  0,  0, -1,  0,  0],
           [ 0,  0,  0,  0,  0, -1,  0],
           [ 0,  0,  0,  0,  0,  0, -1],
           [ 0,  1,  0,  0,  0,  0,  0],
           [ 0,  0,  1,  0,  0,  0,  0],
           [ 0,  0,  0,  1,  0,  0,  0],
           [ 0,  0,  0,  0,  1,  0,  0],
           [ 0,  0,  0,  0,  0,  1,  0]])
    >>> linprog_exemple._calcule_b_ub()
    array([0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 2, 4])
    >>> linprog_exemple._calcule_A_eq()
    array([[ 1, -1, -1,  0,  0,  0,  0],
           [ 0,  1,  0, -1,  1,  0,  0],
           [ 0,  0,  1,  0, -1, -1,  0],
           [ 0,  0,  0,  1,  0,  1, -1]])
    >>> linprog_exemple._calcule_b_eq()
    array([0, 0, 0, 0])
    >>> linprog_exemple.solveur()
    [(('A', 'B'), 4.0), (('A', 'C'), 5.0), (('B', 'D'), 5.0), (('C', 'B'), 1.0), (('C', 'D'), 4.0)]
    >>> linprog_exemple.affiche_solution()
    Problème de flot maximal
    Source : A
    Puit : D
    ┌────────┬─────────┬──────────────┐
    │ Départ │ Arrivée │ Flot maximal │
    ├────────┼─────────┼──────────────┤
    │ A      │ B       │ 4.0          │
    │ A      │ C       │ 5.0          │
    │ B      │ D       │ 5.0          │
    │ C      │ B       │ 1.0          │
    │ C      │ D       │ 4.0          │
    └────────┴─────────┴──────────────┘
    """
    
    def __init__(self, grapheOP: GrapheOP):
        """Initialisation de la classe."""
        self._nx_grapheOP = grapheOP.convertit_nx_graphe()

    def _objectif(self) -> np.array:
        """Vecteurs des coefficients de la fonction à optimiser."""
        graphe = self._nx_grapheOP
        n_edges = len(graphe.edges)
        c = np.array([0] * (n_edges + 2))
        c[0] = -1
        return c

    def _calcule_A_ub(self) -> np.array:
        """Construction de la matrice des contraintes inégalités."""
        graphe = self._nx_grapheOP
        n_edges = len(graphe.edges)
        upper = []
        for up in range(n_edges + 2):
            ligne = [0] * (n_edges + 2)
            ligne[up] = -1
            upper.append(ligne)
        lower = []
        for low in range(1, n_edges + 1):
            ligne = [0] * (n_edges + 2)
            ligne[low] = 1
            lower.append(ligne)
        return np.array(
            np.concatenate(
                (upper, lower), 
                axis=0
            )
        )

    def _calcule_b_ub(self) -> np.array:
        """Construction du vecteur des contraintes inégalités."""
        graphe = self._nx_grapheOP
        n_edges = len(graphe.edges)
        vec = [0] * (n_edges + 2)
        for n1 in graphe.nodes:
            for n2 in graphe.neighbors(n1):
                vec.append(
                    graphe[n1][n2]["capacité"]
                )
        return np.array(vec)

    def _calcule_A_eq(self) -> np.array:
        """"Construction de la matrice des contraintes égalités."""
        graphe = self._nx_grapheOP
        nodes = list(
                graphe.nodes()
        )
        edges = list(
            graphe.edges()
        )
        mat = []
        for id1, n1 in enumerate(nodes):
            ligne = [0] * (len(edges) + 2)
            for edge_id, edge in enumerate(edges):
                if edge in list(graphe.in_edges(n1)):
                    ligne[edge_id + 1] = 1
                else:
                    if edge in list(graphe.out_edges(n1)):
                        ligne[edge_id + 1] = -1
            if id1 == 0:
                ligne[0] = 1
            else:
                if id1 == len(nodes) - 1:
                    ligne[-1] = -1
            mat.append(ligne)
        return np.array(mat)

    def _calcule_b_eq(self) -> np.array:
        """Renvoie le vecteur nul de taille n = nombre de sommets."""
        graphe = self._nx_grapheOP
        n_nodes = len(graphe.nodes)
        return np.array([0] * n_nodes)


    def solveur(self):
        """Résolution du problème de flot maximal."""
        solution = linprog(
            c = self._objectif(), 
            A_eq = self._calcule_A_eq(),
            b_eq = self._calcule_b_eq(), 
            A_ub =  self._calcule_A_ub(),
            b_ub = self._calcule_b_ub(),
            method = "highs"
        )
        return [
            (arrete, flot_max)
            for arrete, flot_max in zip(self._nx_grapheOP.edges, solution.x[1:-1])
        ] 
    
    def _genere_table_solution(self) -> Table:
        """Renvoie une table rich des prérequis."""
        resultat = Table()
        resultat.add_column("Départ")
        resultat.add_column("Arrivée")
        resultat.add_column("Flot maximal")
        for (depart, arrivee), flot_max in self.solveur():
            resultat.add_row(
                depart, arrivee, str(flot_max)
            )
        return resultat
    
    def affiche_solution(self):
        """Affiche directement la table."""
        from rich import print
        print(self._genere_table_solution())
        
    def genere_graphique(self) -> plt.Figure:
        """Visualisation du graphe obtenu."""
        flot_max_graph = nx.DiGraph()
        flot_max_graph.add_weighted_edges_from(
            [
                (depart, arrivee, flot_max)
                for (depart, arrivee), flot_max in self.solveur()
            ],
            weight="flot"
        )
        figure, repere = plt.subplots(figsize=(12, 8))
        positions = nx.nx_agraph.graphviz_layout(flot_max_graph, prog='dot')
        nx.draw_networkx(
            G=flot_max_graph, 
            pos=positions, 
            ax=repere,
            font_size = 14,
            node_color = "skyblue"
        )
        flots = nx.get_edge_attributes(G=flot_max_graph, name="flot")
        nx.draw_networkx_edge_labels(
            G=flot_max_graph,
            pos=positions,
            edge_labels=flots,
            font_size = 12
        )
        repere.set_title("Visualisation du flot maximal", fontsize = 14)
        plt.show()