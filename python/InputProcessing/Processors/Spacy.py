from .. import ProcessorTemplate
from .. import Document
import spacy


class Spacy(
    ProcessorTemplate.TokenizerInterface, 
    ProcessorTemplate.PosTaggerInterface, 
    ProcessorTemplate.LemmatizerInterface, 
    ProcessorTemplate.DeprelAnalyzerInterface):

    def tokenize(self, txt: str, name: str) -> Document.TokenizedDocument:
        pass

    def tag(self, document: Document.TokenizedDocument) -> Document.TaggedDocument:
        pass

    def lemmatize(self, document: Document.TaggedDocument) -> Document.LemmatizedDocument:
        pass

    def deprel(self, document: Document.LemmatizedDocument) -> Document.Document:
        pass