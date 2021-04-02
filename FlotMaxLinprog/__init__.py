"""Description du module FlotMaxLinprog.

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

La commande python -m modelisation permettra d'obtenir cet exemple.
"""

from .graphe_op import (
    GrapheOP,
    Sommet,
    Arrete,
    Poids
)
from .linprog_graph import LinprogGraph

__all__ = [
    "GrapheOP",
    "Sommet",
    "Arrete",
    "Poids",
    "LinprogGraph"
]