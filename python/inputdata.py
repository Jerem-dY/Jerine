# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Ce module est appelé par un script PHP pour traiter les fichiers temporairements stockés sur le serveur et les mettre en ligne dans la base de données.
Il est appelé de la manière suivante : `python inputdata.py test.txt truc.conllu -u 1 -p Spacy Spacy Spacy Spacy -t TXT CoNLLU`, c'est-à-dire 
`python inputdata.py [fichiers] -u [ID utilisateur] -p [tokenizer, tagger, lemmatizer, dependency parser] -t [type de chaque fichier]`

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

import argparse
from FileProcessing.UploadMachine import *
from FileProcessing.DocumentBuilder import *


CONNECTION_PARAMS = {
        'host': "localhost",
        'user': "bourdillat",
        'password': "Uibbnqkbavs09//",
        'db': "bourdillat"
        }



if __name__ == "__main__":

    # On prépare et fait l'acquisition des arguments d'entrée
    argparser = argparse.ArgumentParser(description="Extrait les informations du texte et l'upload sur la base de données.")
    argparser.add_argument('input', help="Les textes à traiter.", type=str, default=[""], nargs='+')
    argparser.add_argument('-p',"--processors" , help="Les processeurs pour compléter les données. [tokenizer, tagger, lemmatizer, dependency parser]", type=str, default=[""], nargs=4)
    argparser.add_argument('-t',"--types" , help="Le type de chaque document.", type=str, default=[""], nargs='+')
    argparser.add_argument('-u', "--user", help="ID de l'utilisateur.", type=int, default=None, nargs=1)
    args = argparser.parse_args()

    # On crée les systèmes de traitement et de mise en ligne
    machine = UploadMachine(len(args.input), args.user[0], CONNECTION_PARAMS)
    docbuilder = DocumentBuilder(args.input, machine.queue, args.types, {k:v for k,v in zip(["tokenizer", "tagger", "lemmatizer", "dependency_analyzer"], args.processors)})


    docbuilder.start()
    machine.run()
    docbuilder.join() # On attend la fin du thread