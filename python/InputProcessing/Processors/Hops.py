from .. import ProcessorTemplate
from .. import Document
#import hopsparser


class Hops(
    ProcessorTemplate.DeprelAnalyzerInterface
):
    def deprel(self, document: Document.LemmatizedDocument) -> Document.Document:
        pass