import pdfplumber
import pytesseract
from PIL import Image

# 🔥 SET TESSERACT PATH HERE
pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract\tesseract.exe"


def extract_text(file_path):

    # 📄 PDF
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    # 🖼 Image (Aadhaar / PAN)
    else:
        return pytesseract.image_to_string(Image.open(file_path))