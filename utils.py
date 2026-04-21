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
    result = {}

    # Clean columns
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Common columns
    common_cols = list(set(df1.columns).intersection(set(df2.columns)))
    df1 = df1[common_cols].astype(str)
    df2 = df2[common_cols].astype(str)

    # 🔹 Similarities
    common_rows = pd.merge(df1, df2)
    result["similarities"] = common_rows

    # 🔹 Missing
    merged = df1.merge(df2, how='outer', indicator=True)

    missing_in_file2 = merged[merged['_merge'] == 'left_only']
    missing_in_file1 = merged[merged['_merge'] == 'right_only']

    result["missing_in_file2"] = missing_in_file2
    result["missing_in_file1"] = missing_in_file1

    # 🔹 Differences (row-level mismatch)
    diff_rows = merged[merged['_merge'] == 'both']

    try:
        cell_diff = df1.compare(df2)
    except:
        cell_diff = "Structure mismatch"

    result["differences"] = cell_diff

    # 🔹 Things to Note (basic insights)
    notes = []

    if len(common_cols) < len(df1.columns):
        notes.append("Some columns are not matching between files")

    if len(missing_in_file2) > 0:
        notes.append(f"{len(missing_in_file2)} rows missing in File 2")

    if len(missing_in_file1) > 0:
        notes.append(f"{len(missing_in_file1)} rows missing in File 1")

    if isinstance(cell_diff, str):
        notes.append("Excel structure mismatch - cannot compare cells properly")

    result["notes"] = notes

    return result
