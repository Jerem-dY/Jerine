import mysql.connector
import argparse
import os
import spacy
import hashlib
from multiprocessing import Pool

connection_params = {
    'host': "localhost",
    'user': "bourdillat",
    'password': "Uibbnqkbavs09//",
    'database': "bourdillat",
}

def hash_doc(doc: str):

    return int(hashlib.blake2b(doc.encode(), digest_size=3, inner_size=3).hexdigest(), 16)

    #return int(hashlib.md5(doc.encode()).hexdigest(), 16)

def process_lemma(token, c):
    # Pour chaque token, on va chercher si son lemme est dans la db
    

    c.execute("select lemma_id from lemma where lemma_form = %s and pos = %s", (token.lemma_, token.pos_))
    lemma_id = c.fetchall()
    found = False

    if lemma_id == []:
        # Si ça n'est pas le cas, on l'insert dedans
        c.execute(f"select max(lemma_id) from lemma")
        max_val = c.fetchall()

        print(max_val[0][0])
        lemma_id = max_val[0][0]+1 if max_val[0][0] != None else 1

    else:
        lemma_id = lemma_id[0][0]
        found = True

    data_lemma = (lemma_id, token.lemma_, token.pos_)
        
    if token.lemma_ not in {None, ""} and token.pos_ not in {None, ""}:

        if not found:
            c.execute("insert into lemma (lemma_id, lemma_form, pos) values (%s, %s, %s)", data_lemma)
            print(f"{data_lemma} inserted")

        return lemma_id
    else:
        return lemma_id-1

def process_token(token, c, lemma_id, token_sent_id, sentence, cmptr_tokens):

    # On récupère le futur id du token (clé primaire)
    c.execute(f"select max(token_id) from token")
    token_id = c.fetchall()
    token_id = token_id[0][0]+1 if token_id[0][0] != None else 1

    if token.i > token.head.i:
        head = cmptr_tokens - abs(token.i - token.head.i)+1
    else:
        head = cmptr_tokens + abs(token.i - token.head.i)+1

    data_token = (token_id, token_sent_id, token.text, lemma_id, sentence, token.dep_, head)
    c.execute("insert into token (token_id, token_sent_id, token_form, lemma, sentence, deprel, head) values (%s, %s, %s, %s, %s, %s, %s)", data_token)


def process_sentence(c, sent, text_id):

    if sent[-1].text == "?":
        sent_type = "INT"
    elif sent[-1].text == "!":
        sent_type = "EXC"
    else:
        sent_type = "DEC"

    c.execute(f"select max(sentence_id) from sentence")
    sentence_id = c.fetchall()
    sentence_id = sentence_id[0][0]+1 if sentence_id[0][0] != None else 1

    data_sentence = (sentence_id, sent_type, text_id)
    c.execute("insert into sentence (sentence_id, type, text_id) values (%s, %s, %s)", data_sentence)

    return sentence_id


def process_document(c, document_name, hash):

    c.execute("select document_id from document where document_id = %s", (hash,))
    document_id = c.fetchall()

    if document_id == []:

        """c.execute(f"select max(document_id) from document")
        document_id = c.fetchall()
        document_id = document_id[0][0]+1 if document_id[0][0] != None else 1"""

        data_document = (hash, document_name)
        c.execute("insert into document (document_id, document_name) values (%s, %s)", data_document)

        document_id = hash

        return document_id
    else:
        raise StopIteration
    


def process_file(txt, login, pwd):
    cmptr_tokens = 0
    lemma_id = 0

    with mysql.connector.connect(**connection_params) as db :

        db.autocommit = True

        with db.cursor(buffered=True) as c:

            c.execute("select documents from user where user.login=%s and user.password=%s", (login, pwd))
            collection_id = c.fetchall()[0][0]

            doc = nlp(txt)

            try:
                document_id = process_document(c, os.path.basename(file), hash_doc(txt))
                c.execute("insert into collection_has_document (collection_id, document_id) values (%s, %s)", (collection_id, document_id))

            except StopIteration:
                print("Skipped redundant document")
                # Ici on pourra assigner le document à l'utilisateur à partir de hash_doc(txt)
                return True

            assert doc.has_annotation("SENT_START")
            for i, sent in enumerate(doc.sents):

                sentence_id = process_sentence(c, sent, document_id)

                for j, token in enumerate(sent):

                    lemma_id = process_lemma(token, c)
                    process_token(token, c, lemma_id, j+1, sentence_id, cmptr_tokens)

                    cmptr_tokens += 1


if __name__ == "__main__":

    

    argparser = argparse.ArgumentParser(description="Extrait les informations du texte et l'upload sur la base de données.")
    argparser.add_argument('input', help="Les textes à traiter.", type=str, default=[""], nargs='+')
    argparser.add_argument('-A', "--authentification", help="Tokens de connexion de l'utilisateur au site.", type=str, default=None, nargs=2)
    args = argparser.parse_args()
    
    nlp = spacy.load("fr_core_news_sm")
    
    lemmas = {}
    data = []
    
    for file in args.input:

        with open(file, mode="r", encoding="utf-8") as f:
            
            process_file(f.read(), args.authentification[0], args.authentification[1])
            
        """    data.append([f.read()])

        p = Pool(len(args.input) if len(args.input) <= 5 else 5)
        p.map(process_file, data)"""
                

            


