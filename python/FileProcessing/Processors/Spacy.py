from .. import ProcessorInterfaces
from .. import Document


class Spacy(
    ProcessorInterfaces.TokenizerInterface, 
    ProcessorInterfaces.PosTaggerInterface, 
    ProcessorInterfaces.LemmatizerInterface, 
    ProcessorInterfaces.DeprelAnalyzerInterface):

    def __init__(self):
        import spacy
        from spacy.tokens import Doc

        self.spacyDoc = Doc
        self.nlp = spacy.load("fr_core_news_sm")

    def tokenize(self, document: Document.RawDocument) -> Document.TokenizedDocument:

        text = document.content
        doc = self.nlp(text)

        tokenized_doc = {'token_forms' : [] ,
            'token_sent_inds' : [] ,
            'sentence_doc_inds' : [] ,
            'cmptr_tokens' : 1,
            'token_doc_ind' : [] ,
            'offset' : [] ,
            'spaceafter' : []}
        
        sentence_doc_inds = 1

        for sent in doc.sents:

            token_sent_inds = 1

            for token in sent:
                tokenized_doc["token_forms"].append(token.text)
                tokenized_doc["offset"].append(token.idx)
                tokenized_doc["spaceafter"].append(1 if token.whitespace_ != "" else 0)

                tokenized_doc["token_sent_inds"].append(token_sent_inds)
                tokenized_doc["sentence_doc_inds"].append(sentence_doc_inds)
                tokenized_doc["token_doc_ind"].append(tokenized_doc["cmptr_tokens"])
                
                tokenized_doc["cmptr_tokens"] += 1
                token_sent_inds += 1


            sentence_doc_inds += 1

        return Document.TokenizedDocument(document, **tokenized_doc)

    def tag(self, document: Document.TokenizedDocument) -> Document.TaggedDocument:

        with self.nlp.select_pipes(enable=["tok2vec", "morphologizer"]):
            doc = self.nlp(self.spacyDoc(self.nlp.vocab, document.token_forms))

        args = {'lemma_pos' : [i.pos_ if i.pos_ not in {"", "\n", "\r", "\t", "\f"} else "X" for i in doc]}

        return Document.TaggedDocument(document, **args)

    def lemmatize(self, document: Document.TaggedDocument) -> Document.LemmatizedDocument:

        with self.nlp.select_pipes(enable=["lemmatizer"]):
            doc = self.nlp(self.spacyDoc(self.nlp.vocab, document.token_forms, pos=document.lemma_pos))

        args = {'lemma_forms' : [i.lemma_ for i in doc]}

        return Document.LemmatizedDocument(document, **args)
    
    def deprel(self, document: Document.LemmatizedDocument) -> Document:
        
        with self.nlp.select_pipes(enable=["tok2vec", "parser"]):
            doc = self.nlp(self.spacyDoc(self.nlp.vocab, document.token_forms, pos=document.lemma_pos, lemmas=document.lemma_forms))

        args = {'deprels' : [i.dep_ if i.dep_ != "" else "dep" for i in doc],
                'heads' : [document.token_sent_inds[tok.head.i] if document.token_sent_inds[tok.head.i] != document.token_sent_inds[tok.i] else 0 for tok in doc]}

        return Document.Document(document, **args)
