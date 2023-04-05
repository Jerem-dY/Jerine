# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue  
Projet de fin de semestre  

Module contenant la classe DocumentBuilder de traitement des documents d'entrée.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''


from threading import Thread
from multiprocessing.pool import ThreadPool
from time import sleep
from benchmark import timeit
from asyncio import Queue, get_event_loop
from .Parsers import *
from .Processors import *
from .Document import *
import sys
import os

MAX_THREADS = 5

class DocumentBuilder(Thread):
    """La classe DocumentBuilder s'occupe de traiter les documents d'entrée sur plusieurs threads et envoie le document finalisé dans la queue de l'UploadMachine.
    """

    def __init__(self, input: list[str], upload_queue: Queue, parsers: list, processors: dict):
        """Le constructeur de la classe.

        :param input: Liste des chemins de fichiers à traiter
        :type input: list[str]
        :param upload_queue: Référence vers la queue de l'UploadMachine
        :type upload_queue: Queue
        :param parsers: Liste des parsers à utiliser pour chaque fichier
        :type parsers: list
        :param processors: Dictionnaire décrivant les différents processeurs de traitement à utiliser
        :type processors: dict
        """
        
        super().__init__()

        self.threads: list = []
        self.upload_queue = upload_queue
        self.loop = get_event_loop()
        
        self.pool = ThreadPool(len(input) if len(input) <= MAX_THREADS else MAX_THREADS)

        self.parsers = {}
        self.processors = {}

        # On instancie chaque parser
        for parser in set(parsers):
            self.parsers[parser] = getattr(sys.modules[__name__], parser)()
            
        # On instancie chaque processeur
        for processor in processors:
                self.processors[processor] = getattr(sys.modules[__name__], processors[processor])()

        # On génère les documents bruts
        self.input: list = []

        for i, text in enumerate(input):
             with open(text, mode="r", encoding="utf-8") as f:
                self.input.append({"doc" : RawDocument(os.path.basename(text), f.read()), "type" : parsers[i]})


    def pipeline(self, text: dict):
        """Fonction principale de traitement d'un document, exécutée dans un thread à part.

        :param text: structure contenant un document brut ("doc") et le parser à utiliser ("type")
        :type text: dict
        """

        print(f"'{text['doc'].name}' travaille...")

        ##################################################

        # Parsing :
        # Le parser fournira au moins un objet de type RawDocument ; en fonction du type de fichier et de son contenu, 
        # il peut fournir des sous-classes, permettant de sauter les étapes non nécessaires.
        doc = self.parsers[text["type"]].parse(text["doc"])


        # Tokenisation : 
        if isinstance(doc, RawDocument):
            doc = self.processors["tokenizer"].tokenize(doc)

        # Etiquetage :
        if isinstance(doc, TokenizedDocument):
            doc = self.processors["tagger"].tag(doc)

        # Lemmatisation :
        if isinstance(doc, TaggedDocument):
            doc = self.processors["lemmatizer"].lemmatize(doc)

        # Analyse syntaxique :
        if isinstance(doc, LemmatizedDocument):
            doc = self.processors["dependency_analyzer"].deprel(doc)
                

        ##################################################
        
        self.loop.call_soon_threadsafe(self.upload_queue.put_nowait, doc)
        print(f"'{text['doc'].name}' a fini !")

    @timeit
    def run(self):
        """Fonction permettant de démarrer le traitement des fichiers fournis.
        """
        
        for result in self.pool.map(self.pipeline, self.input):
            pass

    def close(self):
        """Méthode s'assurant de fermer correctement tous les organes de traitement si une méthode est disponible.
        """

        # Pour chaque parser, on vérifie s'il a une méthode close(), et si oui on l'exécute
        for p in self.parsers:
            if hasattr(self.parsers[p], "close") and callable(self.parsers[p].close):
                self.parsers[p].close()

        # Pour chaque processeur, on vérifie s'il a une méthode close(), et si oui on l'exécute
        for p in self.processors:
            if hasattr(self.processors[p], "close") and callable(self.processors[p].close):
                self.processors[p].close()


    def __del__(self):
        self.close()