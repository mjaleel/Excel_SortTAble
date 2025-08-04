import streamlit as st
import pandas as pd

st.set_page_config(page_title="استخراج الأسماء الرباعية", layout="centered")

st.title("📄 استخراج الأسماء الرباعية من نص عدسة Google")

st.markdown("""
الصق النص هنا (كما نسخته من عدسة Google).  
سيتم تجاهل الأرقام والفواصل، وتحويل كل سطر يحتوي على اسم رباعي أو أكثر إلى جدول Excel.
""")

text_input = st.text_area("✂️ الصق النص هنا:", height=300)

if st.button("📥 تحويل إلى Excel"):
    lines = [line.strip() for line in text_input.split("\n") if line.strip()]
    data = []
    seq = 1

    for line in lines:
        if line.isdigit():
            continue
        if len(line.split()) >= 3:
            data.append([seq, line])
            seq += 1

    if data:
        df = pd.DataFrame(data, columns=["التسلسل", "الاسم الرباعي"])
        st.success(f"✅ تم استخراج {len(df)} اسمًا بنجاح.")
        st.dataframe(df)

        @st.cache_data
        def convert_df_to_excel(df):
            return df.to_excel(index=False, engine="openpyxl")

        excel_bytes = convert_df_to_excel(df)

        st.download_button(
            label="📤 تحميل ملف Excel",
            data=excel_bytes,
            file_name="اسماء_مستخرجة.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ لم يتم العثور على أسماء صالحة.")
