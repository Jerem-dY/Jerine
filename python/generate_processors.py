import sys
import inspect
import json
from InputProcessing.Processors import *
from InputProcessing import ProcessorInterfaces


if __name__ == "__main__":
    #template_classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['ProcessorTemplate']) if inspect.isclass(cls_obj))
    #document_classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['Document']) if inspect.isclass(cls_obj))
    classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['__main__']) if inspect.isclass(cls_obj) 
                  and cls_name not in {"TokenizerInterface", "PosTaggerInterface", "LemmatizerInterface", "DeprelAnalyzerInterface"})

    #classes = classes.difference(template_classes)
    #classes = classes.difference(document_classes)

    processors = {
        "tokenizer" : [],
        "tagger" : [],
        "lemmatizer" : [], 
        "dependency_analyzer" : []
    }

    for cls in classes:

        if issubclass(cls, ProcessorInterfaces.TokenizerInterface):
            processors["tokenizer"].append(cls.__name__)

        if issubclass(cls, ProcessorInterfaces.PosTaggerInterface):
            processors["tagger"].append(cls.__name__)

        if issubclass(cls, ProcessorInterfaces.LemmatizerInterface):
            processors["lemmatizer"].append(cls.__name__)

        if issubclass(cls, ProcessorInterfaces.DeprelAnalyzerInterface):
            processors["dependency_analyzer"].append(cls.__name__)

    
    print(json.dumps(processors))
