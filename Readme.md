# Jérine

Plateforme web de gestion de documents et d'import en fichiers **CoNLL-U et TXT **.  
*Le cahier des charges et autres ressources se trouvent dans [docs/readable](/docs/readable)*  

Le site est accessible ici : [***Jérine***](http://i3l.univ-grenoble-alpes.fr/~bourdillat/Jerine/) 

## Description 
Ce site est une application web (s'exécutant dans un navigateur) mettant à disposition de l'utilisateur un espace de travail de stockage pour déposer des documents tokenisés, segmentés en phrases et analysés syntaxiquement. 
Cette plateforme offre les fonctionnalités suivantes :
- L'importation des fichiers provenant d'autres formats tels que TXT et ConLL-U ;
- La tokenisation, la segmentation en phrases, et l'analyse syntaxique des fichiers importés par différents processeurs (SpaCy et TreeTagger);
- Le tri des fichiers par ordre alphabétique, par phrases, par tokens, par lemmes, par formes, par rapport types/tokens, ainsi que par caractères;
- L'ajout et la suppression de fichiers et de collections;
- La visualisation des fichiers sous forme de représentation graphique des dépendances;
- La recherche de fichiers en fonction de leur titre.

La base de données utilisée est une plateforme qui permet à ses utilisateurs de créer un compte personnel, de s'y connecter et de stocker des fichiers dans divers formats (tels que TXT et ConLL-U), tout en bénéficiant d'une certaine forme de sécurité.

## Documentation :
- [javascript](/docs/js/)

## Base de données :
![diagramme de la base de données](/docs/readable/db.png "base de données de l'application"){: .shadow}

## Dépendances :

### javascript

##### *Runtime*
- [jquery](https://jquery.com/) *>= 3.6.1*  
- [jquery-ui](https://jqueryui.com/)  *>= 1.13.2*  
- [DataTables](https://datatables.net/) *>= 1.13.4* 
- [annodoc](https://spyysalo.github.io/annodoc/)  

##### *Documentation* 
- [JSDoc](https://jsdoc.app/) *>= 4.0.2*  
- [npm](https://www.npmjs.com/) *>= 9.5.0*  

### Python
[python](https://www.python.org/) *>= 3.9.6*  

##### *Runtime*
- numpy *>= 1.23.5*  
- [spacy](https://spacy.io/) *>= 3.5.1*  
- [nltk](https://www.nltk.org/) *>= 3.8.1*  
- [treetaggerwrapper](https://treetaggerwrapper.readthedocs.io/en/latest/) *>= 2.3*  

##### *Documentation*
- [sphinx](https://www.sphinx-doc.org/en/master/) *>= 6.1.3*  
- [sphinx-pyreverse](https://github.com/alendit/sphinx-pyreverse) *>= 0.0.17*  
- [pylint](https://pylint.readthedocs.io/en/latest/) *>= 2.16.1*  

