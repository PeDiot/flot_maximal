# Programmation linéaire et flot maximal dans un réseau de flot

Il s'agit d'un problème travaillé dans le cadre du cours de Supply Chain. Un réseau de flot (aussi appelé réseau de transport) est un graphe orienté où chaque arête possède une capacité et peut recevoir un flot. 

Le but est d'utiliser l'algorithme de programmation linéaire HiGHS pour trouver le flot maximal dans un réseau de flot. La distribution d'électricité dans un réseau électrique peut être un exemple du problème abordé ici.

- Création d'un module `FlotMaxLinprog` pour trouver le flot maximal d'un graphe orienté,
- Module testé,
- Exemple résolu dans le fichier `exemple.ipynb`.
