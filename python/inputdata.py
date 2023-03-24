import mysql.connector
import argparse
import os
import spacy
import hashlib
import itertools
from multiprocessing import Pool


def hash_doc(doc: str):

    return int(hashlib.blake2b(doc.encode(), digest_size=3, inner_size=3).hexdigest(), 16)


def transaction(func, db):

    def wrapper(*args, **kargs):
        db.start_transaction()
        res = func(*args, **kargs)
        db.commit()

        return res

    return wrapper

def insert_forms(cursor, forms):

    cursor.executemany("INSERT INTO form (form_chars) VALUES (%s) ON DUPLICATE KEY UPDATE form_id=form_id;", forms)
    
    ids = []

    for i in forms:
        cursor.execute("SELECT form_id FROM form WHERE form_chars = %s;", i)
        ids.append(cursor.fetchall()[0][0])

    return ids

def insert_lemmas(cursor, lemma_form_ids, lemma_pos):

    data = [i for i in zip(lemma_form_ids, lemma_pos)]
    cursor.executemany("INSERT INTO lemma (lemma_form, pos) VALUES (%s, %s) ON DUPLICATE KEY UPDATE lemma_id=lemma_id;", data)
    
    ids = []

    for i in data:
        cursor.execute("SELECT lemma_id FROM lemma WHERE lemma_form = %s AND pos = %s;", i)
        result = cursor.fetchall()

        if result != []:
            ids.append(result[0][0])
        else:
            ids.append(0)

    return ids

def insert_document(cursor, document_name, content):
    hash = hash_doc(content)
    cursor.execute("select document_id from document where document_id = %s", (hash,))

    if cursor.fetchall() != []:
        return None
    else:
        cursor.execute("insert into document (document_id, document_name) values (%s, %s)", (hash, document_name))
        return hash

def insert_sentences(cursor, type, text_id, sentence_doc_ind):

    #cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    data = [i for i in zip(type, tuple([text_id for i in range(len(type))]), sentence_doc_ind)]
    cursor.executemany("INSERT INTO sentence (type, text_id, sentence_doc_ind) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE sentence_id=sentence_id;", data)
    
    ids = []

    for i in data:
        cursor.execute("SELECT sentence_id FROM sentence WHERE text_id = %s AND sentence_doc_ind = %s;", (text_id, i[2]))
        result = cursor.fetchall()

        if result != []:
            ids.append(result[0][0])
        else:
            ids.append(0)

    #cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    return ids

def insert_tokens(cursor, token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter):

    
    data = [i for i in zip(token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter)]

    #print("len de sentence :", len(sentence))
    #print("len de token_form :", len(token_form))

    #cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    cursor.executemany("INSERT INTO token (token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE token_id=token_id;", data)
    
    #cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    """ids = []

    for i in data:
        cursor.execute("SELECT token_id FROM token WHERE lemma_form = %s AND pos = %s;", i)
        ids.append(c.fetchall()[0][0])

    return ids"""

def insert_in_collection(cursor, user_id, document_id):
    cursor.execute("select documents from user where user_id = %s", (user_id,))

    collection_id = cursor.fetchone()[0]
    cursor.execute("insert into collection_has_document (collection_id, document_id) values (%s, %s)", (collection_id, document_id))


def process_file(file):

    

    with open(file, mode="r", encoding="utf-8") as f:

        with mysql.connector.connect(**PARAMS) as db :

            #db.autocommit = True

            try:
                with db.cursor() as c:


                    txt = f.read()

                    document_id = transaction(insert_document, db)(c, os.path.basename(file), txt)
                    print("Doc id : ", document_id)
                    if (document_id) == None:
                        print("Skipped redundant document")
                        # Rajouter l'ajout du texte à la collection de l'utilisateur (si pas déjà)
                        return
                    
                    transaction(insert_in_collection, db)(c, ID, document_id)

                    token_forms = []
                    lemma_forms = []
                    lemma_pos = []
                    sentence_types = []
                    token_sent_inds = []
                    sentence_doc_inds = []
                    deprels = []
                    heads = []
                    sentences = []
                    offset = []
                    spaceafter = []

                    cmptr_tokens = 0
                    token_doc_ind = []

                    doc = nlp(txt)

                    for i, sent in enumerate(doc.sents):

                        sentence_types.append("DEC")
                        sentence_doc_inds.append(i+1)

                        for j, token in enumerate(sent):

                            cmptr_tokens += 1
                            token_doc_ind.append(cmptr_tokens)
                        
                            token_forms.append((token.text.translate(ESCAPE),))
                            lemma_forms.append((token.lemma_.translate(ESCAPE),))
                            offset.append(token.idx)
                            spaceafter.append(int(1 if token.whitespace_ != "" else 0))
                            lemma_pos.append(token.pos_)
                            token_sent_inds.append(j+1)
                            deprels.append(token.dep_)
                            
                            if token.i > token.head.i:
                                heads.append(cmptr_tokens - abs(token.i - token.head.i))
                            else:
                                heads.append(cmptr_tokens + abs(token.i - token.head.i))

                        sentences.append(j)

                    token_form_ids = transaction(insert_forms, db)(c, token_forms)
                    lemma_form_ids = transaction(insert_forms, db)(c, lemma_forms)

                    lemma_ids = transaction(insert_lemmas, db)(c, lemma_form_ids, lemma_pos)
                    sentence_ids = transaction(insert_sentences, db)(c, sentence_types, document_id, sentence_doc_inds)

                    #print("sentences :", sentences)
                    #print("sentence_ids :", sentence_ids)

                    sentence_ids_stretched = []
                    for i in range(len(sentence_ids)):
                        sentence_ids_stretched += list(itertools.repeat(sentence_ids[i], sentences[i]+1))

                    #print(lemma_ids)
                    transaction(insert_tokens, db)(c, token_sent_inds, token_doc_ind, token_form_ids, lemma_ids, sentence_ids_stretched, deprels, heads, offset, spaceafter)

            except Exception as e:
                print("Can't connect to DB.")
                if db == None:
                    print("Couldn't create db object.")
                if c == None:
                    print("Couldn't create cursor object.")

                print(e)


def init_worker(connection_params, escape_table, user_id):
    global PARAMS
    PARAMS = connection_params

    global ESCAPE 
    ESCAPE = escape_table

    global ID
    ID = user_id[0]


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Extrait les informations du texte et l'upload sur la base de données.")
    argparser.add_argument('input', help="Les textes à traiter.", type=str, default=[""], nargs='+')
    argparser.add_argument('-u', "--user", help="ID de l'utilisateur.", type=int, default=None, nargs=1)
    args = argparser.parse_args()
    
    nlp = spacy.load("fr_core_news_sm")

    
    connection_params = {
    'host': "localhost",
    'user': "bourdillat",
    'password': "Uibbnqkbavs09//",
    'database': "bourdillat",
    }
    

    escape_table = str.maketrans({
        '\n' : r'\n',
        '\t' : r'\t',
        '\r' : r'\r',
        '\f' : r'\f'
    })

    p = Pool(2, initializer=init_worker, initargs=(connection_params, escape_table, args.user))
    p.map(process_file, args.input)
    p.close()
        
