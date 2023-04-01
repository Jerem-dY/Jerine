import sys
import inspect
import json
from InputProcessing.Processors import *
from InputProcessing import ProcessorTemplate


#template_classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['ProcessorTemplate']) if inspect.isclass(cls_obj))
#document_classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['Document']) if inspect.isclass(cls_obj))
classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['__main__']) if inspect.isclass(cls_obj))

print(classes)
#classes = classes.difference(template_classes)
#classes = classes.difference(document_classes)

processors = {
    "tokenizer" : [],
    "tagger" : [],
    "lemmatizer" : [], 
    "dependency_analyzer" : []
}

for cls in classes:

    if issubclass(cls, ProcessorTemplate.TokenizerInterface):
        processors["tokenizer"].append(cls.__name__)

    if issubclass(cls, ProcessorTemplate.PosTaggerInterface):
        processors["tagger"].append(cls.__name__)

    if issubclass(cls, ProcessorTemplate.LemmatizerInterface):
        processors["lemmatizer"].append(cls.__name__)

    if issubclass(cls, ProcessorTemplate.DeprelAnalyzerInterface):
        processors["dependency_analyzer"].append(cls.__name__)

with open("../processors.json", mode="w", encoding="utf-8") as f:
    json.dump(processors, f)
