# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Le parser et producer 'TXT' permet :
- de traiter un fichier texte brut en entrée
- de fournir une reconstitution du texte brut (tout ou partie) en sortie

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

from .. import ParserInterfaces
from ..Document import RawDocument

class TXT(ParserInterfaces.ParserInterface):

    extensions = ["txt", ""]

    def parse(self, txt: str, name: str) -> RawDocument:

        return RawDocument(name, txt)
