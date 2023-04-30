# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Ce module met en place des classes abstraites ayant pour objectif de permettre une implémentation rapide et rigoureuse de processeurs de traitement des textes.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

import abc
from .Document import RawDocument, TokenizedDocument, TaggedDocument, LemmatizedDocument, Document


class TokenizerInterface(metaclass=abc.ABCMeta):
    """Interface visant à implémenter un processeur de tokenisation. Nécessite de définir la méthode 'tokenize' dans la classe fille.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'tokenize') and callable(subclass.tokenize) or NotImplemented)
    
    @abc.abstractmethod
    def tokenize(self, document: RawDocument) -> TokenizedDocument:
        """Méthode permettant la tokenisation d'un texte brut (y compris la segmentation en phrase)

        :param txt: Le texte brut à tokeniser
        :type txt: str
        :param name: le nom du document
        :type name: str
        :raises NotImplementedError: si la fonction n'a pas été implémentée par la classe fille
        :return: le document tokenisé
        :rtype: TokenizedDocument
        """

        raise NotImplementedError
pass

class PosTaggerInterface(metaclass=abc.ABCMeta):
    """Interface visant à implémenter un processeur d'étiquetage morphosyntaxique. Nécessite de définir la méthode 'tag' dans la classe fille.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'tag') and callable(subclass.tag) or NotImplemented)
    
    @abc.abstractmethod
    def tag(self, document: TokenizedDocument) -> TaggedDocument:
        """Méthode permettant l'étiquetage des tokens du document fourni.

        :param document: Le document tokenisé à étiqueter
        :type document: TokenizedDocument
        :raises NotImplementedError: si la fonction n'a pas été implémentée par la classe fille
        :return: le document étiqueté
        :rtype: TaggedDocument
        """

        raise NotImplementedError
pass

class LemmatizerInterface(metaclass=abc.ABCMeta):
    """Interface visant à implémenter un processeur de lemmatisation. Nécessite de définir la méthode 'lemmatize' dans la classe fille.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'lemmatize') and callable(subclass.lemmatize) or NotImplemented)
    
    @abc.abstractmethod
    def lemmatize(self, document: TaggedDocument) -> LemmatizedDocument:
        """Méthode permettant la lemmatisation des tokens du document fourni.

        :param document: le document étiqueté à lemmatiser
        :type document: TaggedDocument
        :raises NotImplementedError: si la fonction n'a pas été implémentée par la classe fille
        :return: le document lemmatisé
        :rtype: LemmatizedDocument
        """

        raise NotImplementedError
pass

class DeprelAnalyzerInterface(metaclass=abc.ABCMeta):
    """Interface visant à implémenter un processeur d'analyse syntaxique en dépendances. Nécessite de définir la méthode 'deprel' dans la classe fille.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'deprel') and callable(subclass.deprel) or NotImplemented)
    
    @abc.abstractmethod
    def deprel(self, document: LemmatizedDocument) -> Document:
        """Méthode permettant l'analyse syntaxique des tokens du document fourni.

        :param document: le document lemmatisé à analyser
        :type document: LemmatizedDocument
        :raises NotImplementedError: si la fonction n'a pas été implémentée par la classe fille
        :return: le document analysé
        :rtype: Document
        """

        raise NotImplementedError
pass