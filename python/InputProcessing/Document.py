# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

from typing import Callable

#TODO : ajouter en arguments au constructeur les données attendues (après les avoir retravaillé)


class RawDocument:
    """Classe représentant un document brut. 
    """

    def __init__(self, name: str, content: str):
        """Constructeur de la classe.

        :param name: Le nom du document
        :type name: str
        :param content: Le contenu du document
        :type content: str
        """
        if not (isinstance(name, str) and isinstance(content, str)) or name == "" or content == "":
            raise TypeError("name and content must be non-empty strings.")
        
        self.name = name
        self.content = content

    
    def __repr__(self):
        return f"Document '{self.name}'\n========================\n\n\"{self.content}\""
    
    def __iter__(self):
        return iter(self.token_forms)


class TokenizedDocument(RawDocument):
    """Classe représentant un document tokenisé par un processeur. 

    :raises ValueError: Lorsque toutes les données nécessaires n'ont pas été livrées
    :raises IndexError: Lorsque les listes ne font pas la même taille (nombre de tokens)
    """

    def _check_arguments(self, type: Callable, doc, expectedArgs: set, **kwargs):
        """Valide les arguments fournis pour créer le document.

        :param type: type attendu pour le document d'entrée
        :type type: Callable
        :param doc: document depuis lequel on construit l'objet
        :type doc: TokenizedDocument ou subclass
        :param expectedArgs: set contenant tous les arguments attendus pour construire l'objet
        :type expectedArgs: set
        :raises TypeError: Si le type de document ne correspond à celui attendu
        :raises ValueError: Si tous les arguments attendus n'ont pas été fournis
        :raises IndexError: Lorsque les listes ne font pas la même taille (nombre de tokens)
        """

        # On vérifie si le document source a bien le type attendu
        if not isinstance(doc, type):
                raise TypeError("Wrong document type provided")

        # On vérifie si tous les arguments nécessaires sont apportés
        if not all(k in kwargs for k in expectedArgs):
            raise ValueError('Required arguments were not provided.')
        

        # On défini une éventuelle longueur attendue s'il s'agit d'une sous-classe de TokenizedDocument, 
        # sinon on vérifie l'intégrité des données entre elles
        if hasattr(doc, 'token_forms'):
            length = len(doc.token_forms)
        else:
            length = -1

        # On vérifie si la taille des listes est la même pour toutes
        for arg in kwargs:
            if isinstance(kwargs[arg], list):
                if length == -1:
                    length = len(kwargs[arg])
                else:
                    if len(kwargs[arg]) != length:
                        raise IndexError("Inconsistency in lists' length")


    def __init__(self, doc: RawDocument, **kwargs):
        """Constructeur de la classe.

        :param doc: le document brut
        :type doc: RawDocument
        """

        # On vérifie l'intégrité des arguments
        self._check_arguments(RawDocument, doc, {
            'token_forms',
            'token_sent_inds',
            'sentence_doc_inds',
            'cmptr_tokens',
            'token_doc_ind',
            'offset',
            'spaceafter'
        }, **kwargs)

        # On met à jour les propriétés de l'objet
        self.__dict__.update(doc.__dict__)
        self.__dict__.update(kwargs)


class TaggedDocument(TokenizedDocument):
    """Classe représentant un document tokenisé et étiqueté par des processeurs.
    """

    def __init__(self, doc: TokenizedDocument, **kwargs):
        """Constructeur de la classe.

        :param doc: Le document source tokenisé
        :type doc: TokenizedDocument
        """

        # On vérifie l'intégrité des arguments
        self._check_arguments(TokenizedDocument, doc, {'lemma_pos'}, **kwargs)

        # On met à jour les propriétés de l'objet
        self.__dict__.update(doc.__dict__)
        self.__dict__.update(kwargs)


class LemmatizedDocument(TaggedDocument):
    """Classe représentant un document tokenisé, étiqueté et lemmatisé par des processeurs.
    """

    def __init__(self, doc: TaggedDocument, **kwargs):
        """Constructeur de la classe.

        :param doc: Le document source étiqueté
        :type doc: TaggedDocument
        """

        # On vérifie l'intégrité des arguments
        self._check_arguments(TaggedDocument, doc, {'lemma_forms'}, **kwargs)

        # On met à jour les propriétés de l'objet
        self.__dict__.update(doc.__dict__)
        self.__dict__.update(kwargs)


class Document(LemmatizedDocument):
    """Classe représentant un document tokenisé, étiqueté, lemmatisé et analysé syntaxiquement par des processeurs.
    """

    def __init__(self, doc: LemmatizedDocument, **kwargs):
        """Constructeur de la classe.

        :param doc: Le document source lemmatisé
        :type doc: LemmatizedDocument
        """

        # On vérifie l'intégrité des arguments
        self._check_arguments(LemmatizedDocument, doc, {'deprels', 'heads'}, **kwargs)

        # On met à jour les propriétés de l'objet
        self.__dict__.update(doc.__dict__)
        self.__dict__.update(kwargs)