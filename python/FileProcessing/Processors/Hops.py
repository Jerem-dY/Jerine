from .. import ProcessorInterfaces
from .. import Document
#import hopsparser


class Hops(
    ProcessorInterfaces.DeprelAnalyzerInterface
):
    def deprel(self, document: Document.LemmatizedDocument) -> Document.Document:
        pass