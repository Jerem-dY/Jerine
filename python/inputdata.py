import argparse
from InputProcessing.UploadMachine import *
from InputProcessing.DocumentBuilder import *


CONNECTION_PARAMS = {
        'host': "localhost",
        'user': "bourdillat",
        'password': "Uibbnqkbavs09//",
        'db': "bourdillat"
        }



if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="Extrait les informations du texte et l'upload sur la base de données.")
    argparser.add_argument('input', help="Les textes à traiter.", type=str, default=[""], nargs='+')
    argparser.add_argument('-p',"--processors" , help="Les processeurs pour compléter les données. [tokenizer, tagger, lemmatizer, dependency analyzer]", type=str, default=[""], nargs=4)
    argparser.add_argument('-t',"--types" , help="Le type de chaque document.", type=str, default=[""], nargs='+')
    argparser.add_argument('-u', "--user", help="ID de l'utilisateur.", type=int, default=None, nargs=1)
    args = argparser.parse_args()


    machine = UploadMachine(len(args.input), args.user[0], CONNECTION_PARAMS)
    docbuilder = DocumentBuilder(args.input, machine.queue, args.types, {k:v for k,v in zip(["tokenizer", "tagger", "lemmatizer", "dependency_analyzer"], args.processors)})


    docbuilder.start()
    machine.run()
    docbuilder.join()