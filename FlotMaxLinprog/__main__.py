"""Description.

Exemple de fonctionnement du module FlotMaxLinprog.
"""

from .graphe_op import (
    GrapheOP,
    Sommet,
    Arrete,
    Poids
)
from .linprog_graph import LinprogGraph

grapheOP = GrapheOP(voisinage={'A': {'B': 4, 'C': 5}, 'B': {'D': 5}, 'C': {'B': 2, 'D': 4}, 'D': {}})
print(grapheOP)
exemple = LinprogGraph(grapheOP)
exemple.affiche_solution()
exemple.genere_graphique()