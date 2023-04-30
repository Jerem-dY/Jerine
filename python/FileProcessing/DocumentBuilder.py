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
from concurrent import futures
from tools import timeit
from asyncio import Queue, get_event_loop
from .Parsers import *
from .Processors import *
from .Document import *
import sys
import os

MAX_THREADS = 2

def init_workers(processors, parsers):

    print("Globals initialized.")

    global PROCESSORS
    PROCESSORS = processors

    global PARSERS 
    PARSERS = parsers


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
        

        self.parsers = {}
        self.processors = {}

        # On instancie chaque parser
        for parser in set(parsers):
            self.parsers[parser] = getattr(sys.modules[__name__], parser)()
            
        # On instancie chaque processeur
        for processor in processors:
                self.processors[processor] = getattr(sys.modules[__name__], processors[processor])()

        
        self.pool = futures.ProcessPoolExecutor(MAX_THREADS, initializer=init_workers, initargs=(self.processors, self.parsers))

        # On génère les documents bruts
        self.input: list = []

        for i, text in enumerate(input):
             with open(text, mode="r", encoding="utf-8") as f:
                self.input.append({"name" : os.path.basename(text), "content" : f.read(), "type" : parsers[i]})

    @staticmethod
    def pipeline(text: dict):
        """Fonction principale de traitement d'un document, exécutée dans un thread à part.

        :param text: structure contenant un document brut ("doc") et le parser à utiliser ("type")
        :type text: dict
        """

        print(f"'{text['name']}' travaille...")

        ##################################################

        # Parsing :
        # Le parser fournira au moins un objet de type RawDocument ; en fonction du type de fichier et de son contenu, 
        # il peut fournir des sous-classes, permettant de sauter les étapes non nécessaires.
        doc = PARSERS[text["type"]].parse(text["content"], text["name"])


        # Tokenisation : 
        if type(doc) is RawDocument:
            doc = PROCESSORS["tokenizer"].tokenize(doc)

        # Etiquetage :
        if type(doc) is TokenizedDocument:
            doc = PROCESSORS["tagger"].tag(doc)

        # Lemmatisation :
        if type(doc) is TaggedDocument:
            doc = PROCESSORS["lemmatizer"].lemmatize(doc)

        # Analyse syntaxique :
        if type(doc) is LemmatizedDocument:
            doc = PROCESSORS["dependency_analyzer"].deprel(doc)
                

        ##################################################
        
        #self.loop.call_soon_threadsafe(self.upload_queue.put_nowait, doc)
        print(f"'{text['name']}' a fini !")

        return doc

    @timeit
    def run(self):
        """Fonction permettant de démarrer le traitement des fichiers fournis.
        """
        
        #res = self.pool.map_async(DocumentBuilder.pipeline, self.input, callback=self.toQueue)

        fs = [self.pool.submit(DocumentBuilder.pipeline, arg) for arg in self.input]

        for result in futures.as_completed(fs):
            self.loop.call_soon_threadsafe(self.upload_queue.put_nowait, result.result())

    def toQueue(self, result):
        print(f"Adding to queue : {result.name}")
        self.loop.call_soon_threadsafe(self.upload_queue.put_nowait, result)

        return True

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