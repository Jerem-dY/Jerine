# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue  
Projet de fin de semestre  

Module contenant les processeurs TreeTagger (tokenisation, étiquetage, lemmatisation).
L'usage de la tokenisation est déconseillé car TreeTagger ne segmente pas en phrase, ainsi tout le texte sera casé dans une seule et même phrase.

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

from .. import ProcessorInterfaces
from .. import Document
import itertools

class TreeTagger(
    ProcessorInterfaces.TokenizerInterface, 
    ProcessorInterfaces.PosTaggerInterface, 
    ProcessorInterfaces.LemmatizerInterface):
    """Classe représentant les processeurs utilisables pour l'outil TreeTagger.
    """

    def __init__(self):
        from treetaggerwrapper import TreeTagger, make_tags
        self.tagger = TreeTagger(TAGLANG='fr', TAGOPT=u'-token -lemma -quiet', TAGDIR='D:\documents\COURS\Master IDL\M1\S1\Modélisation de la langue écrite\TD étiquettage\TreeTagger\TreeTagger')
        self.mk_tags = make_tags

    def tokenize(self, document: Document.RawDocument) -> Document.TokenizedDocument:
        
        
        tags = self.tagger.tag_text(document.content)
        output = self.mk_tags(tags)

        args = {'token_forms' : [i.word for i in output],
            'token_sent_inds' : list(range(1, len(output)+1)),
            'sentence_doc_inds' : list(itertools.repeat(1, len(output))),
            'sentences' : list(itertools.repeat(1, len(output))),
            'cmptr_tokens' : len(output),
            'token_doc_ind' : list(range(1, len(output)+1)),
            'offset' : list(itertools.repeat("NULL", len(output))),
            'spaceafter' : list(itertools.repeat(1, len(output)))}
        
        return Document.TokenizedDocument(document, **args)

    def tag(self, document: Document.TokenizedDocument) -> Document.TaggedDocument:

        tags = self.tagger.tag_text(document.token_forms)
        output = self.mk_tags(tags)

        args = {'lemma_pos' : [i.pos for i in output]}

        return Document.TaggedDocument(document, **args)

    def lemmatize(self, document: Document.TaggedDocument) -> Document.LemmatizedDocument:
        
        tags = self.tagger.tag_text(document.token_forms)
        output = self.mk_tags(tags)

        args = {'lemma_form' : [i.lemma for i in output]}

        return Document.LemmatizedDocument(document, **args)