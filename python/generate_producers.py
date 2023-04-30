import sys
import inspect
import json
from FileProcessing.Parsers import *
from FileProcessing.ParserInterfaces import ProducerInterface


if __name__ == "__main__":

    classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['__main__']) if inspect.isclass(cls_obj))

    parsers = []

    for cls in classes:

        if issubclass(cls, ProducerInterface) and cls.__name__ != "ProducerInterface":

            if hasattr(cls, "extensions") and isinstance(getattr(cls, "extensions"), list):
                parsers.append({"producer" : cls.__name__, "ext" : getattr(cls, "extensions")})
            else:
                parsers.append({"producer" : cls.__name__, "ext" : []})

    
    print(json.dumps(parsers))