from .. import ProcessorInterfaces
from .. import Document
import spacy


class Spacy(
    ProcessorInterfaces.TokenizerInterface, 
    ProcessorInterfaces.PosTaggerInterface, 
    ProcessorInterfaces.LemmatizerInterface, 
    ProcessorInterfaces.DeprelAnalyzerInterface):

    def tokenize(self, document: Document.RawDocument) -> Document.TokenizedDocument:
        pass

    def tag(self, document: Document.TokenizedDocument) -> Document.TaggedDocument:
        pass

    def lemmatize(self, document: Document.TaggedDocument) -> Document.LemmatizedDocument:
        pass

    def deprel(self, document: Document.LemmatizedDocument) -> Document.Document:
        pass