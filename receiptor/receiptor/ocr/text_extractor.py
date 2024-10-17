import io
import base64
import PyPDF2
from docx import Document
from PyPDF2.errors import PdfReadError


class DocumentTextExtractor:

    @staticmethod
    def extract_text_from_attachment(filename: str, data: str) -> str:
        file_extension = DocumentTextExtractor.get_file_extension(filename)
        try:
            if file_extension == '.pdf':
                decoded_data = base64.urlsafe_b64decode(data)
                return DocumentTextExtractor.extract_text_from_pdf(decoded_data)
            elif file_extension == '.docx':
                decoded_data = base64.urlsafe_b64decode(data)
                return DocumentTextExtractor.extract_text_from_docx(decoded_data)
            else:
                return f"Unsupported document type: {file_extension}"
        except PdfReadError as e:
            if "encrypted" in str(e).lower():
                return "Skipped: PDF is encrypted"
            else:
                return f"Error reading PDF: {str(e)}"
        except Exception as e:
            return f"Error processing {file_extension} file: {str(e)}"
    @staticmethod
    def extract_text_from_pdf( pdf_data: bytes) -> str:
        with io.BytesIO(pdf_data) as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    @staticmethod
    def extract_text_from_docx( docx_data: bytes) -> str:
        doc = Document(io.BytesIO(docx_data))
        return "\n".join(para.text for para in doc.paragraphs)

    @staticmethod
    def get_file_extension(filename: str) -> str:
        return '.' + filename.split('.')[-1].lower()