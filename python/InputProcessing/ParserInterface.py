# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Ce module met en place une interface pour rapidement et facilement ajouter des types de fichiers d'entrée et leur traitement préliminaire.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

import abc
from typing import Any


class ParserInterface(metaclass=abc.ABCMeta):
    """Interface visant à implémenter un parser de fichier d'un certain type.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parse') and callable(subclass.parse) or NotImplemented)
    
    @abc.abstractmethod
    def parse(self, txt: str, name: str) -> Any:
        """Méthode permettant le parsing d'un fichier d'un certain type, pour le préparer au traitement et à l'upload.

        :param txt: Le contenu brut du fichier
        :type txt: str
        :param name: le nom du document
        :type name: str
        :raises NotImplementedError: si la fonction n'a pas été implémentée par la classe fille
        :return: le document, soit brut, soit déjà traité à un certain niveau
        :rtype: Any
        """

        raise NotImplementedError
pass