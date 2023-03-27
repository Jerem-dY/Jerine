import mysql.connector
from mysql.connector import errors
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

        t = 3

        while t>0:
            try:
                
                db.start_transaction(isolation_level="READ COMMITTED")
                res = func(*args, **kargs)
                db.commit()
                t = 0
            except errors.Error as e:
                print(e, ": trying again.")
                t -=1

        return res

    return wrapper

def insert_forms(cursor, forms):

    cursor.executemany("INSERT INTO form (form_chars) VALUES (%s) ON DUPLICATE KEY UPDATE form_id=form_id;", forms)
    
    ids = []

    for i in forms:
        cursor.execute("SELECT form_id FROM form WHERE form_chars = %s;", i)
        result = cursor.fetchall()
        
        if result != []:
            ids.append(result[0][0])
        else:
            ids.append(0)


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

        '''cursor.execute("""select document.document_id from document 
            join collection_has_document on collection_has_document.document_id = document.document_id
            join user on user.documents = collection_has_document.collection_id
            where document.document_id = %s and user.user_id = %s""", (hash, ID))'''

        return (hash, True)
    else:
        cursor.execute("insert into document (document_id, document_name) values (%s, %s)", (hash, document_name))
        return (hash, False)

def insert_sentences(cursor, type, text_id, sentence_doc_ind):

    data = [i for i in zip(type, tuple([text_id for j in range(len(type))]), sentence_doc_ind)]
    cursor.executemany("INSERT INTO sentence (type, text_id, sentence_doc_ind) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE sentence_id=sentence_id;", data)
    
    ids = []

    for i in data:
        cursor.execute("SELECT sentence_id FROM sentence WHERE text_id = %s AND sentence_doc_ind = %s;", (text_id, i[2]))
        result = cursor.fetchall()

        if result != []:
            ids.append(result[0][0])
        else:
            ids.append(0)

    return ids

def insert_tokens(cursor, token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter):

    
    data = [i for i in zip(token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter)]

    cursor.executemany("INSERT INTO token (token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE token_id=token_id;", data)

def insert_in_collection(cursor, user_id, document_id):
    cursor.execute("select documents from user where user_id = %s", (user_id,))

    collection_id = cursor.fetchall()[0][0]
    cursor.execute("insert into collection_has_document (collection_id, document_id) values (%s, %s) ON DUPLICATE KEY UPDATE collection_id=collection_id", (collection_id, document_id))


def process_file(file):

    

    with open(file, mode="r", encoding="utf-8") as f:

        db = CONNECTION

        try:
            with db.cursor(prepared=False) as c:


                txt = f.read()

                document_id, is_in_db = transaction(insert_document, db)(c, os.path.basename(file), txt)
                transaction(insert_in_collection, db)(c, ID, document_id)

                print("Doc id : ", document_id)
                if is_in_db:
                    print("Skipped redundant document")
                    return

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
                sentence_ids_stretched = []

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

                
                for i in range(len(sentence_ids)):
                    sentence_ids_stretched += list(itertools.repeat(sentence_ids[i], sentences[i]+1))

                #print(lemma_ids)
                transaction(insert_tokens, db)(c, token_sent_inds, token_doc_ind, token_form_ids, lemma_ids, sentence_ids_stretched, deprels, heads, offset, spaceafter)

        except errors.Error as e:
            print("Can't connect to DB.")
            if db == None:
                print("Couldn't create db object.")
            if c == None:
                print("Couldn't create cursor object.")
             
            print(e)
            print("Rolling back...")
            db.rollback() 


def init_worker(connection, escape_table, user_id):
    global CONNECTION
    CONNECTION = connection

    global ESCAPE 
    ESCAPE = escape_table

    global ID
    ID = user_id[0]


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Extrait les informations du texte et l'upload sur la base de données.")
    argparser.add_argument('input', help="Les textes à traiter.", type=str, default=[""], nargs='+')
    argparser.add_argument('-p',"--processors" , help="Les processeurs pour compléter les données. [tokenizer, tagger, lemmatizer, dependency analyzer]", type=str, default=[""], nargs=4)
    argparser.add_argument('-t',"--types" , help="Le type de chaque document.", type=str, default=[""], nargs='+')
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

    processors = {
        "tokenizer": args.processors[0],
        "tagger": args.processors[1],
        "lemmatizer": args.processors[2],
        "dependency_analyzer": args.processors[3]
    }

    types = args.types

    if len(types) != len(args.input):
        print("Mismatch between number of types and documents. Aborting.")
        exit()

    print(processors)
    print(types)

    connection = mysql.connector.connect(**connection_params)
    connection.autocommit = True

    global CONNECTION
    CONNECTION = connection

    global ESCAPE 
    ESCAPE = escape_table

    global ID
    ID = args.user[0]

    for file in args.input:
        process_file(file)


    """p = Pool(2, initializer=init_worker, initargs=(connection, escape_table, args.user))
    p.map_async(process_file, args.input)
    p.close()"""
        
