# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue  
Projet de fin de semestre  

Module contenant l'UploadMachine, permettant la mise en ligne de documents.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''


from .UploadTask import UploadTask
import asyncio
import aiomysql
from tools import timeit
from .Document import Document



class UploadMachine:
    """Classe représentant l'UploadMachine, une bête féroce destinée à mettre dans la base de données les documents fournis par l'utilisateur.
    Elle communique directement avec le DocumentBuilder.
    """

    def __init__(self, to_treat: int, user_id: int, connection_params: dict):
        """Constructeur de la classe.

        :param to_treat: Nombre de documents à traiter
        :type to_treat: int
        """

        self.user_id = user_id
        self.to_treat = to_treat
        self.queue = asyncio.Queue(to_treat)

        self.forms_lock = asyncio.Lock()
        self.lemmas_lock = asyncio.Lock()
        self.sentences_lock = asyncio.Lock()
        self.tokens_lock = asyncio.Lock()

        self.loop = asyncio.get_event_loop()


        self.connection_pool: aiomysql.Pool = self.loop.run_until_complete(aiomysql.create_pool(**connection_params))

    @timeit
    def run(self):
        """Méthode permettant de démarrer la machine.
        """

        self.tasks = [self.loop.create_task(self.worker()) for i in range(0, self.to_treat)]

        self.loop.run_until_complete(asyncio.wait(self.tasks))


    async def worker(self):
        """Méthode décrivant un worker, unité de travail asynchrone gérant une seule tâche.
        """
        
        doc: Document = await self.queue.get()

        #async with self.connection_pool.acquire() as conn:
        task = UploadTask(self.user_id, doc, self.connection_pool, self.forms_lock, self.lemmas_lock, self.sentences_lock, self.tokens_lock)

        await task.process_file()

        self.to_treat -= 1
        self.queue.task_done()
        print(f"Uploaded : {doc.name}")
        print(f"{self.to_treat} more to go.")
            
