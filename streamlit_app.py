import streamlit as st
import pandas as pd
import io
import re

st.set_page_config(page_title="تحليل أسماء ومبالغ", layout="centered")

st.title("📄 استخراج الأسماء الرباعية مع المبالغ والتسلسل")

st.markdown("""
الصق النص المستخرج من عدسة Google، وسيقوم البرنامج باكتشاف:
- التسلسل (إن وُجد)
- الاسم الرباعي أو أكثر
- المبلغ (إن وُجد)

ويُصدّرهم إلى ملف Excel جاهز.
""")

text_input = st.text_area("✂️ الصق النص هنا:", height=400)

if st.button("📥 تحويل إلى Excel"):
    lines = [line.strip() for line in text_input.split("\n") if line.strip()]
    rows = []

    current = {"تسلسل": "", "الاسم": "", "المبلغ": ""}

    for line in lines:
        if line.isdigit():
            # نعتبره تسلسل إذا لم يُملأ بعد
            if current["تسلسل"] == "":
                current["تسلسل"] = line
            else:
                # ربما يكون اسم مفقود سابقًا
                rows.append(current)
                current = {"تسلسل": line, "الاسم": "", "المبلغ": ""}
        elif re.match(r"^[\d,]+$", line):
            current["المبلغ"] = line
            rows.append(current)
            current = {"تسلسل": "", "الاسم": "", "المبلغ": ""}
        else:
            # سطر يبدو أنه اسم
            if current["الاسم"]:
                current["الاسم"] += " " + line
            else:
                current["الاسم"] = line

    # إضافة آخر اسم إن لم يُضف
    if current["الاسم"]:
        rows.append(current)

    # إنشاء جدول
    df = pd.DataFrame(rows)
    df.columns = ["التسلسل", "الاسم الرباعي", "المبلغ"]

    # عرض النتائج
    st.success(f"✅ تم استخراج {len(df)} سجلًا.")
    st.dataframe(df)

    # حفظ إلى Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='بيانات')

    st.download_button(
        label="📤 تحميل Excel",
        data=output.getvalue(),
        file_name="بيانات_أسماء_ومبالغ.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
