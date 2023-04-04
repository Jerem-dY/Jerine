import sys
import inspect
import json
from InputProcessing.Parsers import *
from InputProcessing.ParserInterface import ParserInterface


if __name__ == "__main__":

    classes = set(cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['__main__']) if inspect.isclass(cls_obj))

    parsers = []

    for cls in classes:

        if issubclass(cls, ParserInterface) and cls.__name__ != "ParserInterface":
            parsers.append(cls.__name__)

    
    print(json.dumps(parsers))