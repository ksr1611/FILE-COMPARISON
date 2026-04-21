import streamlit as st
from utils import read_excel, read_pdf, read_image, compare_text, compare_excel

st.set_page_config(page_title="Document Comparator", layout="wide")

st.title("📄 Document Comparison Tool")

file1 = st.file_uploader("Upload First File", type=["xlsx", "pdf", "png", "jpg", "jpeg"])
file2 = st.file_uploader("Upload Second File", type=["xlsx", "pdf", "png", "jpg", "jpeg"])

if file1 and file2:
    file_type = file1.name.split(".")[-1].lower()

    st.divider()

    if file_type == "xlsx":
    df1 = read_excel(file1)
    df2 = read_excel(file2)

    st.subheader("📊 Excel Comparison")

    result = compare_excel(df1, df2)

    st.write("### ❌ Missing in File 2")
    st.dataframe(result["missing_in_file2"])

    st.write("### ❌ Missing in File 1")
    st.dataframe(result["missing_in_file1"])

    st.write("### 🔍 Cell Differences")
    st.dataframe(result["cell_diff"])

    elif file_type == "pdf":
        text1 = read_pdf(file1)
        text2 = read_pdf(file2)

        st.subheader("📄 PDF Comparison")
        diff = compare_text(text1, text2)

        st.text_area("Differences", diff, height=400)

    elif file_type in ["png", "jpg", "jpeg"]:
        text1 = read_image(file1)
        text2 = read_image(file2)

        st.subheader("🖼 Image OCR Comparison")
        diff = compare_text(text1, text2)

        st.text_area("Differences", diff, height=400)

    else:
        st.error("❌ Unsupported file format")
