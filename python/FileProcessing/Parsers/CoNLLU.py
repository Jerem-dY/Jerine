# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue
Projet de fin de semestre

Le parser et producer 'CoNLLU' permet :
- de traiter un fichier CoNLL-U en entrée
- de fournir une sortie d'un texte (tout ou partie) au format CoNLL-U

Le format CoNLL-U est détaillé ici : https://universaldependencies.org/format.html

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

from .. import ParserInterfaces
from ..Document import *
from enum import IntEnum
import re

class CoNLLU(ParserInterfaces.ParserInterface, ParserInterfaces.ProducerInterface):

    extensions = ["conllu", "csv", "tsv"]


    Columns = IntEnum('Columns', ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC'], start=0)


    def parse(self, txt: str, name: str) -> Document:

        doc = RawDocument(name, txt)

        sentences = doc.content.split("\n\n")
        
        tokenized_doc_data = {
           'token_forms' : [],
            'token_sent_inds' : [],
            'sentence_doc_inds' : [],
            'cmptr_tokens' : 0,
            'token_doc_ind' : [],
            'offset' : [],
            'spaceafter' : []
        }

        is_tagged = False
        tagged_doc_data = {
            'lemma_pos' : []
        }

        is_lemmatized = False
        lemmatized_doc_data = {
            'lemma_forms' : []
        }

        is_analysed = False
        full_doc_data = {'deprels' : [], 'heads' : []}

        for i_sent, sent in enumerate(sentences):

            for i_line, l in enumerate(sent.split('\n')):

                if l == '' or l[0] == '#':
                    continue
                else:
                    data = l.split('\t')

                    if len(data) != 10:
                        print(f"Fichier CoNLLU '{name}' - erreur phrase {i_sent} : mauvais nombre de colonnes ({len(data)}) ligne {i_line} : \n{l}")
                        continue

                    tokenized_doc_data['token_forms'].append(data[CoNLLU.Columns.FORM])
                    tokenized_doc_data['token_sent_inds'].append(data[CoNLLU.Columns.ID])
                    tokenized_doc_data['sentence_doc_inds'].append(i_sent+1)
                    tokenized_doc_data['cmptr_tokens'] += 1
                    tokenized_doc_data['token_doc_ind'].append(tokenized_doc_data['cmptr_tokens'])


                    ### Spaceafter

                    tokenized_doc_data['spaceafter'].append(0 if re.match(r"SpaceAfter=No", data[CoNLLU.Columns.MISC]) != None else 1)

                    ### Offset

                    if (m := re.match(r"TokenRange=([0-9]+):[0-9]+", data[CoNLLU.Columns.MISC])) != None:
                        # Si l'offset est spécifié dans le fichier CoNLLU :

                        tokenized_doc_data['offset'].append(int(m.group(1)))

                    elif i_sent > 1 or i_line > 1:
                        # Si l'offset n'est pas spécifié et que l'on n'est pas sur le premier token :

                        tokenized_doc_data['offset'].append(
                            tokenized_doc_data['offset'][-1] + len(tokenized_doc_data['token_forms'][-2]) + tokenized_doc_data['spaceafter'][-2] if len(tokenized_doc_data['spaceafter']) > 1 else 0
                            )
                        
                    else:
                        tokenized_doc_data['offset'].append(0)


                    ### POS

                    if data[CoNLLU.Columns.UPOS] != '_':
                        is_tagged = True
                        tagged_doc_data["lemma_pos"].append(data[CoNLLU.Columns.UPOS])

                    else:
                        tagged_doc_data["lemma_pos"].append("X")

                    ### LEMMA

                    if data[CoNLLU.Columns.LEMMA] != '_':
                        is_lemmatized = True
                        lemmatized_doc_data['lemma_forms'].append(data[CoNLLU.Columns.LEMMA])

                    else:
                        lemmatized_doc_data['lemma_forms'].append("")


                    ### DEPRELS

                    if data[CoNLLU.Columns.DEPREL] != '_' and data[CoNLLU.Columns.HEAD] != '_':
                        is_analysed = True
                        full_doc_data['deprels'].append(data[CoNLLU.Columns.DEPREL])
                        full_doc_data['heads'].append(data[CoNLLU.Columns.HEAD])

                    else:
                        full_doc_data['deprels'].append("dep")
                        full_doc_data['heads'].append(0)


        doc = TokenizedDocument(doc, **tokenized_doc_data)

        if is_tagged:
            doc = TaggedDocument(doc, **tagged_doc_data)

            if is_lemmatized:
                doc = LemmatizedDocument(doc, **lemmatized_doc_data)

                if is_analysed:
                    doc = Document(doc, **full_doc_data)

        
        return doc

    def produce(self, data: list) -> str:

        return ""