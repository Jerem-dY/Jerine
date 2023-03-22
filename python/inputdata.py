import mysql.connector
import argparse
import os
import spacy
import hashlib
import itertools
from multiprocessing import Pool


def hash_doc(doc: str):

    return int(hashlib.blake2b(doc.encode(), digest_size=3, inner_size=3).hexdigest(), 16)


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
            ids.append(-1)

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

    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    data = [i for i in zip(type, tuple([text_id for i in range(len(type))]), sentence_doc_ind)]
    cursor.executemany("INSERT INTO sentence (type, text_id, sentence_doc_ind) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE sentence_id=sentence_id;", data)
    
    ids = []

    for i in data:
        cursor.execute("SELECT sentence_id FROM sentence WHERE text_id = %s AND sentence_doc_ind = %s;", (text_id, i[2]))
        result = cursor.fetchall()

        if result != []:
            ids.append(result[0][0])
        else:
            ids.append(-1)

    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    return ids

def insert_tokens(cursor, token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter):

    
    data = [i for i in zip(token_sent_ind, [token_doc_ind for i in range(len(token_form))], token_form, lemma, sentence, deprel, head, offset, spaceafter)]

    print("len de sentence :", len(sentence))
    print("len de token_form :", len(token_form))

    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    cursor.executemany("INSERT INTO token (token_sent_ind, token_doc_ind, token_form, lemma, sentence, deprel, head, offset, spaceafter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE token_id=token_id;", data)
    
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    """ids = []

    for i in data:
        cursor.execute("SELECT token_id FROM token WHERE lemma_form = %s AND pos = %s;", i)
        ids.append(c.fetchall()[0][0])

    return ids"""



def process_file(file):

    

    with open(file, mode="r", encoding="utf-8") as f:

        with mysql.connector.connect(**PARAMS) as db :

            db.autocommit = True

            print(PARAMS)
            print(db)

            try:
                with db.cursor() as c:
                    txt = f.read()

                    if (document_id := insert_document(c, os.path.basename(file), txt)) == None:
                        print("Skipped redundant document")
                        # Rajouter l'ajout du texte à la collection de l'utilisateur (si pas déjà)
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

                    doc = nlp(txt)

                    for i, sent in enumerate(doc.sents):

                        sentence_types.append("DEC")
                        sentence_doc_inds.append(i+1)

                        for j, token in enumerate(sent):

                            cmptr_tokens += 1
                        
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

                    token_form_ids = insert_forms(c, token_forms)
                    lemma_form_ids = insert_forms(c, lemma_forms)

                    lemma_ids = insert_lemmas(c, lemma_form_ids, lemma_pos)
                    sentence_ids = insert_sentences(c, sentence_types, document_id, sentence_doc_inds)

                    print("sentences :", sentences)
                    print("sentence_ids :", sentence_ids)

                    sentence_ids_stretched = []
                    for i in range(len(sentence_ids)):
                        sentence_ids_stretched += list(itertools.repeat(sentence_ids[i], sentences[i]))


                    insert_tokens(c, token_sent_inds, document_id, token_form_ids, lemma_ids, sentence_ids_stretched, deprels, heads, offset, spaceafter)
            except Exception as e:
                print("Can't connect to DB.")
                if db == None:
                    print("Couldn't create db object.")
                if c == None:
                    print("Couldn't create cursor object.")

                print(e)


def init_worker(connection_params, escape_table):
    global PARAMS
    PARAMS = connection_params

    global ESCAPE 
    ESCAPE = escape_table


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Extrait les informations du texte et l'upload sur la base de données.")
    argparser.add_argument('input', help="Les textes à traiter.", type=str, default=[""], nargs='+')
    argparser.add_argument('-A', "--authentification", help="Tokens de connexion de l'utilisateur au site.", type=str, default=None, nargs=2)
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

    p = Pool(2, initializer=init_worker, initargs=(connection_params, escape_table))
    p.map(process_file, args.input)
    p.close()
        
