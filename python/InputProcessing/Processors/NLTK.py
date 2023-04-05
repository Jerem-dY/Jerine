# -*- coding: utf-8 -*-

'''
INFORMATIONS GENERALES
=========================================================================
Cours de Python - M1 Sciences du Langage parcours Industries de la Langue  
Projet de fin de semestre  

Module contenant les processeurs NLTK (tokenisation, étiquetage, lemmatisation et analyse syntaxique en dépendances).

INFORMATIONS SUR LE MODULE
=========================================================================
:auteur: Jérémy Bourdillat <Jeremy.Bourdillat@etu.univ-grenoble-alpes.fr>
:version: 1.0
Python ver. 3.11.1
'''

from .. import ProcessorInterfaces
from .. import Document
import itertools
import os
import signal

class NLTK(ProcessorInterfaces.TokenizerInterface, 
    ProcessorInterfaces.PosTaggerInterface, ProcessorInterfaces.DeprelAnalyzerInterface):


    def __init__(self):

        from nltk.parse.corenlp import CoreNLPServer
        from nltk.parse.corenlp import CoreNLPDependencyParser
        import nltk.tokenize
        import subprocess


        self.server = subprocess.Popen(
        """cd /home/IdL/2022/bourdillat/nltk_data/stanford-corenlp-4.5.4 ; java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
        > -serverProperties StanfordCoreNLP-french.properties \
        > -preload tokenize,ssplit,pos,parse \
        > -status_port 9004  -port 9004 -timeout 15000""", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, preexec_fn=os.setsid) 
        
        self.parser = CoreNLPDependencyParser('http://localhost:9004')
        self.tagger = CoreNLPDependencyParser('http://localhost:9004', tagtype='pos')
        self.splitter = nltk.data.load('tokenizers/punkt/PY3/french.pickle')

    def tokenize(self, document: Document.RawDocument) -> Document.TokenizedDocument:

        
        json_result = self.parser.api_call(document.content, properties={'annotators': 'tokenize, ssplit'})
        
        # Segmentation en phrases :
        sentences = self.tokenizer.tokenize("Ceci est un test. Encore un. Et un autre ! Hehe...")

        #Tokenisation des phrases :
        tokens = [list(self.parser.tokenize(s)) for s in sentences]

        args = {'token_forms' : [],
            'token_sent_inds' : [],
            'sentence_doc_inds' : [],
            'sentences' : [],
            'cmptr_tokens' : 0,
            'token_doc_ind' : [],
            'offset' : [],
            'spaceafter' : []}
        
        for i, sentence in enumerate(json_result['sentences']):

            args['token_forms'] += [j['word'] for j in json_result['sentences'][i]['tokens']]
            args['cmptr_tokens'] += len(json_result['sentences']['tokens'])
            args['sentences'] += itertools.repeat(i+1, len(sentence)['tokens'])
            args['token_doc_ind'] += list(range(args['cmptr_tokens'], args['cmptr_tokens']+len(sentence)['tokens']+1))
            args['offset'] += [j['characterOffsetBegin'] for j in [i]['tokens']]
            args['spaceafter'] += [0 if j['after'] == '' else 1 for j in [i]['tokens']]
            args['token_sent_inds'] += [j['index'] for j in [i]['tokens']]

        return Document.TokenizedDocument(document, **args)
    
    def tag(self, document: Document.TokenizedDocument) -> Document.TaggedDocument:

        output = self.tagger.tag(document.token_forms)

        tags = [i[1] for i in output]

        args = {'lemma_pos' : tags}

        return Document.TaggedDocument(document, **args)
    
    def deprel(self, document: Document.LemmatizedDocument) -> Document:

        parse_tree, = list(self.parser.parse(document.token_forms))

        output = [parse_tree.nodes[i] for i in range(1, len(parse_tree.nodes))]

        args = {
            'deprels' : [i["rel"] for i in output], 
            'heads': [i["head"] for i in output]}


        return Document.Document(document, **args)
    
    def close(self):
        os.killpg(self.server.pid, signal.SIGTERM)

    
    def __del__(self):
        os.killpg(self.server.pid, signal.SIGTERM)