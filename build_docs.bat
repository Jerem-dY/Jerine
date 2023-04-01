@ECHO OFF

rem Ce script permet de générer toutes les documentations

rem documentation javascript
cd .\js
call jsdoc -c .\jsdoc_config.json


rem documentation php

rem documentation python
cd ..\docs
call .\make.bat clean
cd ..\python
call pyreverse --output svg --project InputProcessing --filter-mode ALL --all-ancestors InputProcessing --output-directory ..\docs\uml
call sphinx-apidoc -o ..\docs . --ext-autodoc --ext-imgmath --ext-githubpages --force
cd ..\docs
call .\make.bat html
