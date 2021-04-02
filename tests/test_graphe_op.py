#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests pour la classe Graphe_OP.
"""

import coverage
import pytest
from FlotMaxLinprog import *


def test_init():
    g = GrapheOP(voisinage={})
    assert isinstance(g, GrapheOP)

def test_egalite():
    g1 = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )
    g2 = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )
    assert g1 == g2

def test_repr():
    """Dunder __repr__ ."""
    g = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )

    assert repr(g) == "GrapheOP(voisinage={'A': {'B': 1}, 'B': {}, 'C': {}})"

def test_par_sommets_arretes():
    """Pour coller à la définition mathématiques."""
    alternatif = GrapheOP.par_sommets_arretes(
        sommets=["A", "B", "C"], arretes=[("A", "B", 1)]
    )
    attendu = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )
    assert alternatif == attendu

def test_arrete_rendondante():
    """Doit boguer."""
    with pytest.raises(ValueError):
        alternatif = GrapheOP.par_sommets_arretes(
            sommets=["A", "B", "C"], arretes=[(("A", "B"), 1), (("A", "B"), 2)]
        )

def test_sommets():
    """Teste l'attribut sommets."""
    g = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )
    assert list(g.sommets) == list("ABC")

def test_arretes():
    """Teste l'attribut arretes."""
    g = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )
    assert list(g.arretes) == [("A", "B", 1)]

def test_voisins():
    g = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {},
            "C": {},
        }
    )
    assert g["A"] == {"B": 1}

def test_par_str_ord():
    """Constructeur alternatif."""
    essai = GrapheOP.par_str_ordonne(
        """
A B 1
"""
    )
    attendu = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {}
        }
    )
    assert essai == attendu

def test_adjacence():
    graphe = GrapheOP(
        voisinage={
            "A": {"B": 1, "C": 2},
            "B": {"A": 3, "C": 4},
            "C": {"C": 5},
        }
    )
    attendu = [
        [0, 1, 2],
        [3, 0, 4],
        [0, 0, 5],
    ]
    assert graphe.adjacence == attendu

def test_graphe_ordonne():
    """Matrice symétrique."""
    graphe = GrapheOP(
        voisinage={
            "A": {"B": 1, "C": 2},
            "B": {"A": 3, "C": 4},
            "C": {"C": 5},
        }
    )
    assert graphe.est_ordonne
    graphe_s = GrapheOP(
        voisinage={
            "A": {"B": 1},
            "B": {"A": 1, "C": 4},
            "C": {"B": 4},
        }
    )
    assert not graphe_s.est_ordonne
    
def test_convertit_nx_graphe():
    """Test la conversion du graphe."""
    graphe = GrapheOP(
        voisinage={
            'A': {'B': 4, 'C': 5}, 
            'B': {'D': 5}, 
            'C': {'B': 2, 'D': 4}, 
            'D': {}
        }
    )
    graphe_nx = graphe.convertit_nx_graphe()
    sommets = [
        sommet for sommet in graphe_nx.nodes
    ]
    arretes = [
        arrete for arrete in graphe_nx.edges
    ]
    sommets_attendus = ['A', 'B', 'C', 'D']
    arretes_attendues = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'B'), ('C', 'D')]
    assert sommets == sommets_attendus
    assert arretes == arretes_attendues
    

