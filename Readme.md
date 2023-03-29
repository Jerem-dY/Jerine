# Bourdillat-Adjoudj

Plateforme web de gestion de documents et d'import/export en fichiers **CoNLL-U, TXT et XML**.  
*Le cahier des charges et autres ressources se trouvent dans [docs/readable](/docs/readable)*  

Le site est accessible ici : [***Adjoudj-Bourdillat***](http://i3l.univ-grenoble-alpes.fr/~bourdillat/Bourdillat-Adjoudj/) 

## Description 
Ce site est une application web (s'éxecutant dans un navigateur) mettant à disposition de l'utilisateur un espace de travail et un stockage pour déposer des documents tokenisés, segmentés en phrases et analysés syntaxiquement. L'application permet l'import de fichiers de type *texte brut*, *XML* ou *CoNLL-U*. Il est possible de compléter les informations manquantes à l'aide des processeurs disponibles (spaCy, stanza, nltk, etc.). L'export des documents dans les mêmes formats que ceux cités précédemment est possible. L'utilisateur a aussi accès à diverses visualisations de ses données, elles aussi exportables.  
et ça sera tout.


## Wiki :
- [Sécurité](https://gricad-gitlab.univ-grenoble-alpes.fr/idl2022-2023/bourdillat-adjoudj/-/wikis/S%C3%A9curit%C3%A9)  
- [Performances](https://gricad-gitlab.univ-grenoble-alpes.fr/idl2022-2023/bourdillat-adjoudj/-/wikis/Performances)  

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

##### *Documentation* 
- [JSDoc](https://jsdoc.app/) *>= 4.0.2*  
- [npm](https://www.npmjs.com/) *>= 9.5.0*  

### Python
[python](https://www.python.org/) *>= 3.9.6*  

##### *Runtime*
- numpy *>= 1.23.5*  
- [spacy](https://spacy.io/) *>= 3.5.1*  
- [nltk](https://www.nltk.org/) *>= 3.8.1*  

##### *Documentation*
- [sphinx](https://www.sphinx-doc.org/en/master/) *>= 6.1.3*  
- [sphinx-pyreverse](https://github.com/alendit/sphinx-pyreverse) *>= 0.0.17*  
- [pylint](https://pylint.readthedocs.io/en/latest/) *>= 2.16.1*  


### Rust

##### *Runtime* 
- [cpython](https://docs.rs/cpython/latest/cpython/) *>= 0.7.1*  

##### *Documentation*
- [rustdoc](https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html) *>= 1.68.0*  