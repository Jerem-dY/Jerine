from .. import ParserInterface
from ..Document import RawDocument

class TXT(ParserInterface.ParserInterface):

    extensions = ["txt", ""]

    def parse(self, txt: str, name: str) -> RawDocument:

        return RawDocument(name, txt)
