from InputProcessing.DocumentBuilder import *
from InputProcessing.UploadMachine import *
import glob
import os


CONNECTION_PARAMS = {
        'host': "localhost",
        'user': "bourdillat",
        'password': "Uibbnqkbavs09//",
        'db': "bourdillat"
        }


if __name__ == '__main__':


    files = glob.glob("testCorpus/*.txt")


    machine = UploadMachine(len(files), 3, CONNECTION_PARAMS)
    docbuilder = DocumentBuilder(files, machine.queue, ["TXT" for i in files], {
        "tokenizer" : "Spacy",
        "tagger" : "Spacy",
        "lemmatizer" : "Spacy", 
        "dependency_analyzer" : "Spacy"
    })


    docbuilder.start()
    machine.run()
    docbuilder.join()