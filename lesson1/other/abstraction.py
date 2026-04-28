from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass


class PDFDocument(Document):
    pass

class HTMLDocument(Document):
    def generate(self) -> str:
        return "HTML document generated"

class WordDocument(Document):
    def generate(self) -> str:
        return "Word document generated"


pdf_document = PDFDocument()
