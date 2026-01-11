# الملف: app.py
import streamlit as st
import pandas as pd
from PIL import Image

# --- الهوية الرسمية للمشروع ---
st.set_page_config(page_title="Smart Grocery - Jordan", layout="wide")

# تفعيل اللغتين
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
def t(ar, en): return ar if st.session_state.lang == 'ar' else en

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except: st.info("Logo Placeholder")
    
    st.markdown(f"### Lujan Al Najar & Juod Hejjawi")
    st.divider()
    page = st.radio(t("القائمة", "Menu"), [t("الرئيسية", "Home"), t("المخزن الذكي", "Smart Inventory"), t("عن المشروع", "About")])

# --- المنطق المطور (المعدل عن ملف recommender 2) ---
def advanced_recommend(pref_type):
    # عينة بيانات من الـ Dataset الخاص بكِ
    products = [
        {"name": "تمام (Tamam)", "price": 4.2, "local": True, "quality": 5},
        {"name": "الطاحونة (Al-Tahoona)", "price": 3.5, "local": True, "quality": 4},
        {"name": "أمريكانا (Americana)", "price": 5.0, "local": False, "quality": 4},
    ]
    
    scored = []
    for p in products:
        score = 0
        if pref_type == "local" and p['local']: score += 10
        if pref_type == "price": score += (1 / p['price']) * 50
        if pref_type == "brand": score += p['quality'] * 5
        scored.append({"name": p['name'], "score": score})
    
    return sorted(scored, key=lambda x: x['score'], reverse=True)

# --- شاشة العرض الرئيسية ---
if page == t("الرئيسية", "Home"):
    st.title(t("المساعد الذكي للتسوق 🛒", "Smart Grocery Assistant 🛒"))
    
    col1, col2 = st.columns(2)
    with col1:
        user = st.radio(t("اختر مستخدم للتجربة:", "Select Demo User:"), ["Lujan (Price)", "Juod (Local Support)"])
    
    if st.button(t("تشغيل محرك التوصية", "Run AI Recommendation")):
        pref = "price" if "Lujan" in user else "local"
        results = advanced_recommend(pref)
        st.success(f"{t('أفضل خيار:', 'Top Choice:')} {results[0]['name']}")
        st.write(t("تحليل الأوزان بناءً على تفضيلاتك:", "Weight analysis based on your preferences:"))
        st.bar_chart(pd.DataFrame(results).set_index('name'))

elif page == t("المخزن الذكي", "Smart Inventory"):
    st.header(t("📸 تحديث المخزن", "📸 Update Inventory"))
    st.camera_input(t("صوّر الفاتورة (محاكاة OCR)", "Scan Bill (OCR Simulation)"))

elif page == t("عن المشروع", "About"):
    st.info(f"Prepared by: Lujan Al Najar & Juod Hejjawi")
    st.write("Subject: Smart Grocery AI System - Jordan Market")