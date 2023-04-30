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
    ProcessorInterfaces.PosTaggerInterface, 
    ProcessorInterfaces.LemmatizerInterface):
    """Classe représentant les processeurs utilisables pour l'outil TreeTagger.
    """

    def __init__(self):
        from treetaggerwrapper import TreeTagger, make_tags
        self.tagger = TreeTagger(TAGLANG='fr', TAGOPT=u'-token -lemma -quiet')
        self.mk_tags = make_tags

    """def tokenize(self, document: Document.RawDocument) -> Document.TokenizedDocument:
        
        
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
        
        return Document.TokenizedDocument(document, **args)"""

    def tag(self, document: Document.TokenizedDocument) -> Document.TaggedDocument:

        output = []

        for token in document.token_forms:
            tags = self.tagger.tag_text(token)
            output.append(self.mk_tags(tags)[0].pos if len(self.mk_tags(tags)) > 0 and self.mk_tags(tags)[0].pos != "" else "X")

        args = {'lemma_pos' : self._convert_tagset(output)}

        return Document.TaggedDocument(document, **args)

    def lemmatize(self, document: Document.TaggedDocument) -> Document.LemmatizedDocument:
        
        output = []
        for token in document.token_forms:
            tags = self.tagger.tag_text(token)
            output.append(self.mk_tags(tags)[0].lemma if len(self.mk_tags(tags)) > 0 and self.mk_tags(tags)[0].lemma != "" else "NULL")

        args = {'lemma_forms' : output}

        return Document.LemmatizedDocument(document, **args)
    

    def _convert_tagset(self, tags: list):

        new = []

        table = {'NUM' : 'NUM', 
                'SYM' : 'SYM', 
                'PUN:cit' : 'PUNCT', 
                'X' : 'X', 
                'VER:futu' : 'VERB', 
                'PRO:IND' : 'PRON', 
                'PRP:det' : 'ADP', 
                'VER:pres' : 'VERB', 
                'PRO' : 'PRON', 
                'ADJ' : 'ADJ', 
                'PRP' : 'ADP', 
                'VER:ppre' : 'VERB', 
                'VER:pper' : 'VERB', 
                'PUN' : 'PUNCT', 
                'VER:impf' : 'VERB', 
                'KON' : 'CCONJ', 
                'SENT' : 'PUNCT', 
                'DET:ART' : 'DET', 
                'PRO:DEM' : 'PRON', 
                'VER:subp' : 'VERB', 
                'ADV' : 'ADV', 
                'NAM' : 'PROPN', 
                'VER:infi' : 'VERB', 
                'DET:POS' : 'DET', 
                'NOM' : 'NOUN', 
                'PRO:PER' : 'PRON', 
                'ABR' : 'NOUN', 
                'VER:cond' : 'VERB'}
        
        for token in tags:
            new.append(table[token] if token in table else "X")

        return new
    
    def close(self):
        del self.tagger