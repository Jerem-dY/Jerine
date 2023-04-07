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
import aiomysql
import hashlib
import textwrap
import itertools
from typing import Callable
from .Document import Document


VERBOSE = True

def hash_doc(doc: str):
    return int(hashlib.blake2b(doc.encode(), digest_size=3, inner_size=3).hexdigest(), 16)


def transaction(func: Callable):

    async def wrapper(self: 'UploadTask', *args, **kwargs):

        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.SSCursor) as cur:
                out = await func(self, cur, *args, **kwargs)
                await conn.commit()
        
        return out
    return wrapper
    


def verbose(func: Callable):

    async def wrapper(self: 'UploadTask', *args, **kwargs):

        if VERBOSE:
            print(f"§ [{self.document.name:<40}]\t{func.__name__:<20}\t❔")

        try:
            out = await func(self, *args, **kwargs)

            if VERBOSE:
                print(f"§ [{self.document.name:<40}]\t{func.__name__:<20}\t👍")

            return out
        
        except Exception as e:
            if VERBOSE:
                error = textwrap.indent(str(e), '\t> ')
                print(f"§ [{self.document.name:<40}]\t{func.__name__:<20}\t❌ ({error})\n")


        
    
    return wrapper


class UploadTask:
    """Classe représentant une tâche de mise en ligne d'un document dans la base de données.
    """

    def __init__(self, user_id: int, doc: Document, pool: aiomysql.Pool, forms_lock, lemmas_lock, sentences_lock, tokens_lock):
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

        self.user_id = user_id
        self.document: Document = doc

        self.forms_lock = forms_lock
        self.lemmas_lock = lemmas_lock
        self.sentences_lock = sentences_lock
        self.tokens_lock = tokens_lock

        self.pool = pool


    async def process_file(self):
        """Méthode principale permettant la mise en ligne du document.
        """


        print(f"### [{self.document.name:<12}]\tDEMARRE. ⭕")

        document_id, is_in_db = await self.insert_document()
        await self.insert_in_collection(document_id)

        async with self.forms_lock:
            token_form_ids = await self.insert_forms(self.document.token_forms)
            lemma_form_ids = await self.insert_forms(self.document.lemma_forms)

        async with self.lemmas_lock:
            lemma_ids = await self.insert_lemmas(lemma_form_ids, self.document.lemma_pos)
        
        async with self.sentences_lock:
            sentence_ids = await self.insert_sentences(document_id, list(dict.fromkeys(self.document.sentence_doc_inds)))


        # token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter
        async with self.tokens_lock:

            await self.insert_tokens(self.document.token_sent_inds, 
                                     self.document.token_doc_ind, 
                                     token_form_ids, 
                                     lemma_ids, 
                                     self.document.sentence_doc_inds, 
                                     self.document.deprels, 
                                     self.document.heads, 
                                     self.document.offset, 
                                     self.document.spaceafter)

        print(f"§ [{self.document.name:<12}]\tTERMINE. ✅")

    @transaction
    @verbose
    async def insert_document(self, cursor: aiomysql.SSCursor) -> tuple:
        """Méthode effectuant l'insertion du document dans la table "document" de la base de données.
        """

        hash = hash_doc(self.document.content)

        # On vérifie si le document a déjà été uploadé par le passé :
        await cursor.execute("select document_id from document where document_id = %s", (hash,))
        result = await cursor.fetchall()

        # Si le document est déjà dans la base de données :
        if result != []:
            return (hash, True)
        else:
            await cursor.execute("insert into document (document_id, document_name) values (%s, %s)", (hash, self.document.name))
            return (hash, False)
        

    @transaction
    @verbose
    async def insert_in_collection(self, cursor: aiomysql.SSCursor, document_id: int):
        """Méthode effectuant l'insertion du document dans le champ "documents" d'un utilisateur de la base de données.
        """

        await cursor.execute("select documents from user where user_id = %s", (self.user_id,))
        collection_id = await cursor.fetchall()

        await cursor.execute("insert into collection_has_document (collection_id, document_id) values (%s, %s) ON DUPLICATE KEY UPDATE collection_id=collection_id", (collection_id[0][0], document_id))
        

    @transaction
    @verbose
    async def insert_forms(self, cursor: aiomysql.SSCursor, forms: list[str]):
        """Méthode effectuant l'insertion des formes du document dans la table "form" de la base de données.
        """

        await cursor.executemany("INSERT INTO form (form_chars) VALUES (%s) ON DUPLICATE KEY UPDATE form_id=LAST_INSERT_ID(form_id);", forms)
        
        ids = []

        for i in forms:
            await cursor.execute("SELECT form_id FROM form WHERE form_chars = %s;", i)
            result = await cursor.fetchall()
            
            if result != []:
                ids.append(result[0][0])
            else:
                ids.append(0)
        
        #ids = list(range(cursor.lastrowid-len(forms), cursor.lastrowid+1))


        return ids


    @transaction
    @verbose
    async def insert_lemmas(self, cursor: aiomysql.SSCursor, lemma_form_ids, lemma_pos):
        """Méthode effectuant l'insertion des lemmes du document dans la table "lemma" de la base de données.
        """


        data = [i for i in zip(lemma_form_ids, lemma_pos)]
        await cursor.executemany("INSERT INTO lemma (lemma_form, pos) VALUES (%s, %s) ON DUPLICATE KEY UPDATE lemma_id=LAST_INSERT_ID(lemma_id);", data)
        
        ids = []

        for i in data:
            await cursor.execute("SELECT lemma_id FROM lemma WHERE lemma_form = %s AND pos = %s;", i)
            result = await cursor.fetchall()

            if result != []:
                ids.append(result[0][0])
            else:
                ids.append(0)
        
        #ids = list(range(cursor.lastrowid-len(lemma_pos), cursor.lastrowid+1))

        return ids


    @transaction 
    @verbose
    async def insert_sentences(self, cursor: aiomysql.SSCursor, text_id, sentence_doc_ind):
        """Méthode effectuant l'insertion des phrases du document dans la table "sentence" de la base de données.
        """

        data = [i for i in zip(itertools.repeat("DEC", len(sentence_doc_ind)), itertools.repeat(text_id, len(sentence_doc_ind)), sentence_doc_ind)]
        await cursor.executemany("INSERT INTO sentence (type, text_id, sentence_doc_ind) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE sentence_id=LAST_INSERT_ID(sentence_id);", data)
        
        ids = []

        for i in data:
            await cursor.execute("SELECT sentence_id FROM sentence WHERE text_id = %s AND sentence_doc_ind = %s;", (text_id, i[2]))
            result = await cursor.fetchall()

            if result != []:
                ids.append(result[0][0])
            else:
                ids.append(0)
        #ids = list(range(cursor.lastrowid, cursor.lastrowid+len(sentence_doc_ind)))

        return ids


    @transaction        
    @verbose
    async def insert_tokens(self, cursor: aiomysql.SSCursor, token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter):
        """Méthode effectuant l'insertion des tokens du document dans la table "token" de la base de données.
        """

        data = [i for i in zip(token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter)]

        await cursor.executemany("INSERT INTO token (token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE token_id=LAST_INSERT_ID(token_id);", data)


        

