# Bourdillat-Adjoudj

Plateforme web de gestion de documents et d'import/export en fichiers **CoNLL-U, TXT et XML**.  
*Le cahier des charges et autres ressources se trouvent dans [docs/readable](/docs/readable)*  

Le site est accessible ici : [***Adjoudj-Bourdillat***](http://i3l.univ-grenoble-alpes.fr/~bourdillat/Bourdillat-Adjoudj/)  

## Wiki :
- [Sécurité](https://gricad-gitlab.univ-grenoble-alpes.fr/idl2022-2023/bourdillat-adjoudj/-/wikis/S%C3%A9curit%C3%A9)

## Base de données :
[diagramme de la base de données](/docs/readable/db.png "base de données de l'application"){: .shadow}

## Dépendances :

### javascript
- [jquery](https://jquery.com/) *>= 3.6.1*  
- [jquery-ui](https://jqueryui.com/)  *>= 1.13.2*  
- [DataTables](https://datatables.net/) *>= 1.13.4*  

### Python
[python](https://www.python.org/) *>= 3.9.6*  

#### Runtime
- numpy *>= 1.23.5*  
- [spacy](https://spacy.io/) *>= 3.5.1*  
- [nltk](https://www.nltk.org/) *>= 3.8.1*  

#### Documentation
- [sphinx](https://www.sphinx-doc.org/en/master/) *>= 6.1.3*  
- [sphinx-pyreverse](https://github.com/alendit/sphinx-pyreverse) *>= 0.0.17*  
- [pylint](https://pylint.readthedocs.io/en/latest/) *>= 2.16.1*  


### Rust
- [cpython](https://docs.rs/cpython/latest/cpython/) *>= 0.7.1*  