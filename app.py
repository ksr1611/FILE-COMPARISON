if file_type == "xlsx":
    df1 = read_excel(file1)
    df2 = read_excel(file2)

    st.subheader("📊 Excel Comparison")

    result = compare_excel(df1, df2)

    # ✅ Similarities
    st.write("## ✅ Similarities")
    st.dataframe(result["similarities"])

    # ❌ Differences
    st.write("## ❌ Differences")
    st.dataframe(result["differences"])

    # ⚠️ Missing
    st.write("## ⚠️ Missing in File 2")
    st.dataframe(result["missing_in_file2"])

    st.write("## ⚠️ Missing in File 1")
    st.dataframe(result["missing_in_file1"])

    # 🧠 Notes
    st.write("## 🧠 Things to Note")
    for note in result["notes"]:
        st.write("- " + note)
