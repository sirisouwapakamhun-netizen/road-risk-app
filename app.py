
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ระบบประเมินความเสี่ยงอุบัติเหตุ",
    page_icon="🚨",
    layout="centered"
)

EPDO_MEAN  = 1.461124
EPDO_STD   = 1.810367
SER_MEAN   = 0.142887
SER_STD    = 0.544385
KM_MEAN    = 126.241977
KM_STD     = 205.019965

def calc_epdo(fatal, serious, minor):
    return (fatal * 9.5) + (serious * 3.5) + (minor * 1.0)

def standardize(value, mean, std):
    return (value - mean) / std

st.title("🚨 ระบบประเมินความเสี่ยงอุบัติเหตุ")
st.markdown("""
**การพัฒนาระบบค้นหาจุดอันตรายแฝงและวิเคราะห์ปัจจัยการเสียชีวิตจากอุบัติเหตุ**  
บนโครงข่ายถนนของกระทรวงคมนาคม  
กรอกข้อมูลจากหน้างาน ระบบจะคำนวณ EPDO และประเมินระดับความเสี่ยงโดยอัตโนมัติ
""")

st.divider()
st.subheader("📋 กรอกข้อมูลอุบัติเหตุ")

col1, col2, col3 = st.columns(3)
with col1:
    fatal = st.number_input("ผู้เสียชีวิต (คน)", min_value=0, max_value=50, value=0, step=1)
with col2:
    serious = st.number_input("ผู้บาดเจ็บสาหัส (คน)", min_value=0, max_value=50, value=0, step=1)
with col3:
    minor = st.number_input("ผู้บาดเจ็บเล็กน้อย (คน)", min_value=0, max_value=100, value=0, step=1)

km = st.number_input("ตำแหน่งกิโลเมตรบนสายทาง (KM)", min_value=0.0, max_value=2000.0, value=0.0, step=0.1)

st.divider()

if st.button("🔍 ประเมินความเสี่ยง", type="primary", use_container_width=True):

    epdo_raw = calc_epdo(fatal, serious, minor)
    epdo_scaled    = standardize(epdo_raw, EPDO_MEAN, EPDO_STD)
    serious_scaled = standardize(serious, SER_MEAN, SER_STD)
    km_scaled      = standardize(km, KM_MEAN, KM_STD)

    if epdo_scaled > 1.817 and serious_scaled > 3.408 and km_scaled > -0.615:
        level = "high"
    elif epdo_scaled > 1.817:
        level = "mid"
    else:
        level = "low"

    st.divider()
    st.subheader("📊 ผลการประเมิน")

    if level == "high":
        st.error("### ⚠️ ความเสี่ยงสูง — ส่งทีมกู้ภัยด่วน\n\nอุบัติเหตุนี้มีลักษณะตรงกับรูปแบบที่มีความเสี่ยงเสียชีวิตสูง ควรส่งทีมกู้ภัยและแจ้งโรงพยาบาลทันที")
    elif level == "mid":
        st.warning("### ◉ ต้องเฝ้าระวัง — ติดตามสถานการณ์\n\nความรุนแรงอยู่ในระดับสูงกว่าปกติ แต่ยังไม่ถึงเกณฑ์วิกฤต ควรติดตามและเตรียมทีมสำรองไว้")
    else:
        st.success("### ✓ ความเสี่ยงต่ำ — ไม่จำเป็นต้องส่งทีมเพิ่ม\n\nค่า EPDO ต่ำกว่าเกณฑ์ อุบัติเหตุนี้มีความรุนแรงในระดับปกติ")

    st.subheader("📌 ข้อมูลที่ใช้ประเมิน")
    st.markdown(f"""
| ตัวแปร | ค่าจริง | ค่า Standardized |
|---|---|---|
| EPDO (คำนวณอัตโนมัติ) | {epdo_raw:.2f} | {epdo_scaled:.3f} |
| ผู้บาดเจ็บสาหัส | {serious} | {serious_scaled:.3f} |
| ตำแหน่ง KM | {km:.1f} | {km_scaled:.3f} |
    """)

    st.caption(f"สูตร EPDO = (ผู้เสียชีวิต × 9.5) + (ผู้บาดเจ็บสาหัส × 3.5) + (ผู้บาดเจ็บเล็กน้อย × 1.0) = {epdo_raw:.2f}")

st.divider()

with st.expander("📖 เกณฑ์การประเมิน (จาก Decision Tree)"):
    st.markdown("""
| ระดับ | เงื่อนไข (ค่า Standardized) | การดำเนินการ |
|---|---|---|
| 🔴 สูง | EPDO > 1.817 และ ผู้บาดเจ็บสาหัส > 3.408 และ KM > −0.615 | ส่งทีมกู้ภัยด่วน |
| 🟡 กลาง | EPDO > 1.817 แต่ไม่ตรงเงื่อนไขด้านบน | เฝ้าระวัง |
| 🟢 ต่ำ | EPDO ≤ 1.817 | ไม่จำเป็นต้องส่งทีมเพิ่ม |

ระบบนี้เป็น Prototype ที่พัฒนาจากกฎ Decision Tree  
ซึ่งได้จากการวิเคราะห์ข้อมูลอุบัติเหตุ 268,358 แถว  
Accuracy 98.30% | F1-Score 98.31%
    """)

st.caption("สิริเสาวภา คำหาญ | รหัส 6723765613 | ดท.224 | มหาวิทยาลัยธรรมศาสตร์ 2569")
