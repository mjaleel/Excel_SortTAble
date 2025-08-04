import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="استخراج الأسماء الرباعية", layout="centered")

st.title("📄 استخراج الأسماء الرباعية من نص عدسة Google")

st.markdown("""
- الصق الأسماء (الرباعية) من عدسة Google في المربع الأول.  
- وإذا لديك مبالغ مطابقة، الصقها في المربع الثاني (اختياري).  
- يتم مطابقة كل مبلغ مع الاسم حسب الترتيب.
""")

# مربع نص الأسماء
text_input = st.text_area("✂️ الصق الأسماء هنا:", height=300)

# مربع نص اختياري للمبالغ
amount_input = st.text_area("💰 (اختياري) الصق المبالغ فقط:", height=200)

if st.button("📥 تحويل إلى Excel"):
    names = [line.strip() for line in text_input.split("\n") if line.strip()]
    amounts = [line.strip() for line in amount_input.split("\n") if line.strip()]

    if not names:
        st.warning("⚠️ لم يتم إدخال أي أسماء.")
    else:
        data = []
        for i, name in enumerate(names):
            if len(name.split()) >= 3:
                amount = amounts[i] if i < len(amounts) else ""
                data.append([i + 1, name, amount])

        df = pd.DataFrame(data, columns=["التسلسل", "الاسم الرباعي", "المبلغ"])

        st.success(f"✅ تم استخراج {len(df)} اسمًا بنجاح.")
        st.dataframe(df)

        # حفظ إلى ملف Excel في الذاكرة
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='بيانات')

        st.download_button(
            label="📤 تحميل ملف Excel",
            data=output.getvalue(),
            file_name="اسماء_ومبالغ.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
