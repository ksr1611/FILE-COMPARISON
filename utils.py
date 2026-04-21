import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image
import difflib

# If running locally on Windows, uncomment and set path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_excel(file):
    return pd.read_excel(file)

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def read_image(file):
    img = Image.open(file)
    return pytesseract.image_to_string(img)

def compare_text(text1, text2):
    diff = difflib.unified_diff(
        text1.splitlines(),
        text2.splitlines(),
        lineterm=""
    )
    return "\n".join(diff)

def compare_excel(df1, df2):
    try:
        return df1.compare(df2)
    except:
        return "⚠️ Excel structure mismatch (columns/rows not same)"
