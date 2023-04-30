# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Ce module met en place des interfaces pour rapidement et facilement ajouter des types de fichiers d'entrée et leur traitement préliminaire, 
de même que pour le traitement de données de sortie.

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


class ProducerInterface(metaclass=abc.ABCMeta):
    """Interface visant à implémenter un traitement des données dans la DB pour une sortie textuelle spécifique.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'produce') and callable(subclass.produce) or NotImplemented)
    
    @abc.abstractmethod
    def produce(self, data: list) -> str:
        """Méthode traitant les données préalablement récupérées de la base de données pour les mettre en forme en une sortie textuelle

        :param data: les données de la DB, en liste de phrases à traiter
        :type data: list
        :raises NotImplementedError: si la fonction n'a pas été implémentée par la classe fille
        :return: une mise en forme textuelle des données récupérées
        :rtype: str
        """

        raise NotImplementedError