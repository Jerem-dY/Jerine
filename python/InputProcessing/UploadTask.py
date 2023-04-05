# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue  
Projet de fin de semestre  

Module contenant la classe UploadTask destinée à l'UploadMachine.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''


import asyncio
from .Document import Document


class UploadTask:
    """Classe représentant une tâche de mise en ligne d'un document dans la base de données.
    """

    def __init__(self, doc: Document, forms_lock, lemmas_lock, sentences_lock, tokens_lock):
        """Constructeur de la classe.

        :param doc: Le document finalisé à mettre en ligne
        :type doc: Document
        :param forms_lock: Le lock des formes de l'UploadMachine partagé entre les tâches
        :type forms_lock: _type_
        :param lemmas_lock: Le lock des lemmes de l'UploadMachine partagé entre les tâches
        :type lemmas_lock: _type_
        :param sentences_lock: Le lock des phrases de l'UploadMachine partagé entre les tâches
        :type sentences_lock: _type_
        :param tokens_lock: Le lock des tokens de l'UploadMachine partagé entre les tâches
        :type tokens_lock: _type_
        """

        self.document: Document = doc

        self.forms_lock = forms_lock
        self.lemmas_lock = lemmas_lock
        self.sentences_lock = sentences_lock
        self.tokens_lock = tokens_lock


    async def process_file(self):
        """Méthode principale permettant la mise en ligne du document.
        """

        print(f"### [{self.document.name:<12}]\tDEMARRE. ⭕")

        await self.insert_document()
        await self.insert_in_collection()

        async with self.forms_lock:
            await self.insert_forms()
            await self.insert_forms()

        async with self.lemmas_lock:
            await self.insert_lemmas()
        
        async with self.sentences_lock:
            await self.insert_sentences()

        async with self.tokens_lock:
            await self.insert_tokens()

        print(f"§ [{self.document.name:<12}]\tTERMINE. ✅")

    async def insert_document(self):
        """Méthode effectuant l'insertion du document dans la table "document" de la base de données.
        """

        print(f"§ [{self.document.name:<12}]\tinsert_document\t❔")
        await asyncio.sleep(0.1)
        print(f"§ [{self.document.name:<12}]\tinsert_document\t👍")

    async def insert_in_collection(self):
        """Méthode effectuant l'insertion du document dans la table "document_has_collection" de la base de données.
        """

        print(f"§ [{self.document.name:<12}]\tinsert_in_collection\t❔")
        await asyncio.sleep(0.1)
        print(f"§ [{self.document.name:<12}]\tinsert_in_collection\t👍")

    async def insert_forms(self):
        """Méthode effectuant l'insertion des formes du document dans la table "form" de la base de données.
        """

        print(f"§ [{self.document.name:<12}]\tinsert_forms\t❔")
        await asyncio.sleep(3.6)
        print(f"§ [{self.document.name:<12}]\tinsert_forms\t👍")

    async def insert_lemmas(self):
        """Méthode effectuant l'insertion des lemmes du document dans la table "lemma" de la base de données.
        """

        print(f"§ [{self.document.name:<12}]\tinsert_lemmas\t❔")
        await asyncio.sleep(4.0)
        print(f"§ [{self.document.name:<12}]\tinsert_lemmas\t👍")

    async def insert_sentences(self):
        """Méthode effectuant l'insertion des phrases du document dans la table "sentence" de la base de données.
        """

        print(f"§ [{self.document.name:<12}]\tinsert_sentences\t❔")
        await asyncio.sleep(7.5)
        print(f"§ [{self.document.name:<12}]\tinsert_sentences\t👍")

    async def insert_tokens(self):
        """Méthode effectuant l'insertion des tokens du document dans la table "token" de la base de données.
        """

        print(f"§ [{self.document.name:<12}]\tinsert_tokens\t❔")
        await asyncio.sleep(1.2)
        print(f"§ [{self.document.name:<12}]\tinsert_tokens\t👍")