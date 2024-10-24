import PyPDF2
from docx import Document
from PIL import Image
import pytesseract

class FileHandler:
    @staticmethod
    def extract_text_from_pdf(file_path):
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def extract_text_from_docx(file_path):
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    @staticmethod
    def extract_text_from_image(file_path):
        return pytesseract.image_to_string(Image.open(file_path))