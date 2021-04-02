"""Description.

Tests pour la classe LinprogGraph.
"""

import coverage
import pytest
import networkx as nx
import numpy as np
from FlotMaxLinprog import *

@pytest.fixture
def linprog_graph_test():
    return LinprogGraph(
        GrapheOP(
            voisinage={
                'A': {'B': 4, 'C': 5}, 
                'B': {'D': 5}, 
                'C': {'B': 2, 'D': 4},
                'D': {}
            }
        )
    )

def test_objectif(linprog_graph_test):
    """Test."""
    sortie = linprog_graph_test._objectif()
    attendu = np.array([-1,  0,  0,  0,  0,  0,  0])
    
    assert (sortie == attendu).all
    
def test_calcule_A_ub(linprog_graph_test):
    """Test."""
    sortie = linprog_graph_test._calcule_A_ub()
    attendu = np.array(
        [
            [-1,  0,  0,  0,  0,  0,  0],
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
            [ 0,  0,  0,  0,  0,  1,  0]
        ]
    )
    assert (sortie == attendu).all

def test_calcule_b_ub(linprog_graph_test):
    """Test."""
    sortie = linprog_graph_test._calcule_b_ub()
    attendu = np.array([0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 2, 4])
    assert (sortie == attendu).all
    

def test_calcule_A_eq(linprog_graph_test):
    """Test."""
    sortie = linprog_graph_test._calcule_A_eq()
    attendu = np.array(
        [
            [ 1, -1, -1,  0,  0,  0,  0],
            [ 0,  1,  0, -1,  1,  0,  0],
            [ 0,  0,  1,  0, -1, -1,  0],
            [ 0,  0,  0,  1,  0,  1, -1]
        ]
    )
    assert (sortie == attendu).all
    
def test_calcule_b_eq(linprog_graph_test):
    """Test."""
    sortie = linprog_graph_test._calcule_b_eq()
    attendu = np.array([0, 0, 0, 0])
    assert (sortie == attendu).all 

def test_solveur(linprog_graph_test):
    """Teste le solveur."""
    sortie = linprog_graph_test.solveur()
    attendu = [
        (('A', 'B'), 4.0),
        (('A', 'C'), 5.0),
        (('B', 'D'), 5.0),
        (('C', 'B'), 1.0),
        (('C', 'D'), 4.0)
    ]
    assert (sortie == attendu)
