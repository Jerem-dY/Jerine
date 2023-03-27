from enum import StrEnum
import spacy

class Text:

    def __init__(self, name):
        self.name = name

        self.token_forms = []
        self.lemma_forms = []
        self.lemma_pos = []
        self.sentence_types = []
        self.token_sent_inds = []
        self.sentence_doc_inds = []
        self.deprels = []
        self.heads = []
        self.sentences = []
        self.offset = []
        self.spaceafter = []

        self.cmptr_tokens = 0
        self.token_doc_ind = []
        self.sentence_ids_stretched = []


pass

class DocType(StrEnum):
    CONLLU = "CoNLL-U"
    TXT = "TXT"
    XML = "XML"


class Pipeline:

    def __init__(self, texts: list):
        pass

pass



# texts : [{"name": "nom.txt", "content":"blablabla", "type":"TXT"}]
def pipeline(texts: list, pipeline: dict) -> list:

    to_insert = []

    for doc in texts:
        if(doc["type"] == DocType.CONLLU):
            # traitement spécifique CoNLL-U ici
            texts.remove(doc)
            to_insert.append(Text(doc["name"]))
            continue

        if(doc["type"] == DocType.XML):
            # traitement spécifique XML ici
            texts.remove(doc)
            to_insert.append(Text(doc["name"]))
            continue


    ### VARIABLES TO FILL

    ###
    
    # Tokenizing

    if(pipeline["tokenizer"] == "spacy"):

        nlp = spacy.load("fr_core_news_sm")
        docs = []

        for doc in list(nlp.pipe(texts, disable=["tagger", "parser", "ner"])):
            t = Text()

            for i, sent in enumerate(doc.sents):
                
                t.sentence_types.append("DEC")
                t.sentence_doc_inds.append(i+1)

                for j, token in enumerate(sent):

                    t.cmptr_tokens += 1
                    t.token_doc_ind.append(t.cmptr_tokens)
                
                    t.token_forms.append((token.text.translate(ESCAPE),))
                    t.offset.append(token.idx)
                    t.spaceafter.append(int(1 if token.whitespace_ != "" else 0))
                    t.lemma_forms.append((token.lemma_.translate(ESCAPE),))
                    t.deprels.append(token.dep_)
                    t.lemma_pos.append(token.pos_)
                    t.token_sent_inds.append(j+1)
                    
                    if token.i > token.head.i:
                        t.heads.append(t.cmptr_tokens - abs(token.i - token.head.i))
                    else:
                        t.heads.append(t.cmptr_tokens + abs(token.i - token.head.i))

                t.sentences.append(j)

pass