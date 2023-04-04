from .. import ParserInterface
from ..Document import RawDocument

class TXT(ParserInterface.ParserInterface):

    def parse(self, txt: str, name: str) -> RawDocument:

        return RawDocument(name, txt)
