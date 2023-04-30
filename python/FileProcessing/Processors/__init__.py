# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Ce package regroupe les wrappers de traitement pour divers systèmes comme spaCy, HOPS, stanza, etc.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

from pathlib import Path
from importlib import import_module


"Imports all symbols from all modules in the package"
"From : https://gist.github.com/andgineer/141f97164aaea12215cf9a2aed332c1d"

for module_path in Path(__file__).parent.glob('*.py'):
    if module_path.is_file() and not module_path.stem.startswith('_'):
        module = import_module(f'.{module_path.stem}', package=__package__)
        symbols = [symbol for symbol in module.__dict__ if not symbol.startswith("_")]
        globals().update({symbol: getattr(module, symbol) for symbol in symbols})