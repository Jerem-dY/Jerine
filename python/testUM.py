from InputProcessing.DocumentBuilder import *
from InputProcessing.UploadMachine import *
import glob
import os


if __name__ == '__main__':


    files = glob.glob("testCorpus/*.txt")


    machine = UploadMachine(len(files), 3)
    docbuilder = DocumentBuilder(files, machine.queue, ["TXT" for i in files], {
        "tokenizer" : "Spacy",
        "tagger" : "TreeTagger",
        "lemmatizer" : "TreeTagger", 
        "dependency_analyzer" : "Spacy"
    })


    docbuilder.start()
    machine.run()
    docbuilder.join()