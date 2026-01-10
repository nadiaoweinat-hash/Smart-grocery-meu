import streamlit as st
import pandas as pd

# --- 1. إعدادات الصفحة والهوية (MEU Identity) ---
st.set_page_config(page_title="Smart Grocery AI - MEU", layout="wide")

# تفعيل اللغتين (Arabic/English Toggle)
if 'lang' not in st.session_state: st.session_state.lang = 'ar'

def t(ar, en):
    return ar if st.session_state.lang == 'ar' else en

# --- 2. القائمة الجانبية (معلومات الفريق والجامعة) ---
with st.sidebar:
    # محاولة عرض الشعار (اختياري)
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.info("Smart Grocery AI")

    st.markdown("### Middle East University (MEU)")
    st.markdown(f"**Course:** Introduction to AI")
    st.markdown(f"**Instructor:** Dr. Mohammed Shambour")
    st.divider()
    
    st.markdown("### Developed By:")
    st.info("**Lujain Alnajar**\n\nID: 202410697")
    st.info("**Jude Hajjawi**\n\nID: 202411895")
    
    st.divider()
    
    # زر تبديل اللغة
    lang_btn = st.radio("Language / اللغة", ['العربية', 'English'])
    if lang_btn == 'العربية': st.session_state.lang = 'ar'
    else: st.session_state.lang = 'en'
    
    st.divider()
    page = st.radio(t("القائمة", "Menu"), [t("الرئيسية", "Home"), t("المخزن الذكي", "Smart Inventory"), t("عن المشروع", "About Project")])

# --- 3. محرك الذكاء الاصطناعي (Logic Core) ---
def advanced_recommend(pref_type):
    # بيانات المنتجات (Knowledge Base)
    products = [
        {"name": "Tamam Chicken", "price": 4.20, "local": True, "quality": 5, "origin": "Jordan"},
        {"name": "Al-Tahoona", "price": 3.50, "local": True, "quality": 4, "origin": "Jordan"},
        {"name": "Imported Brand X", "price": 5.50, "local": False, "quality": 4, "origin": "USA"},
        {"name": "Generic Import", "price": 3.00, "local": False, "quality": 3, "origin": "China"},
    ]
    
    scored = []
    # خوارزمية الأوزان (Weighted Scoring Algorithm)
    for p in products:
        score = 0
        # 1. دعم المنتج المحلي
        if pref_type == "local" and p['local']: score += 10
        # 2. حساسية السعر (كلما قل السعر زاد السكور)
        if pref_type == "price": score += (1 / p['price']) * 20
        # 3. الجودة والبراند
        if pref_type == "brand": score += p['quality'] * 3
        
        scored.append({"name": p['name'], "score": round(score, 2), "details": p})
    
    # ترتيب النتائج تنازلياً حسب السكور
    return sorted(scored, key=lambda x: x['score'], reverse=True)

# --- 4. واجهة التطبيق (UI) ---

if page == t("الرئيسية", "Home"):
    st.title(t("🛒 المساعد الذكي للتسوق", "🛒 Smart Grocery Assistant"))
    st.caption(t("نظام دعم اتخاذ القرار باستخدام الذكاء الاصطناعي", "AI-Powered Decision Support System"))
    st.divider()

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(t("تفضيلات المستخدم", "User Preferences"))
        # اختيار السيناريو (Lujain vs Jude)
        user_scenario = st.selectbox(
            t("اختر شخصية التجربة:", "Select Demo Persona:"),
            ["Lujain (Budget Focus)", "Jude (Local Support)", "Quality Seeker"]
        )
        
        pref_map = {
            "Lujain (Budget Focus)": "price",
            "Jude (Local Support)": "local",
            "Quality Seeker": "brand"
        }
        
        if st.button(t("تشغيل التحليل 🚀", "Run Analysis 🚀")):
            selected_pref = pref_map[user_scenario]
            results = advanced_recommend(selected_pref)
            
            # حفظ النتائج للجلسة
            st.session_state.results = results
            st.session_state.ran = True

    with col2:
        if 'ran' in st.session_state and st.session_state.ran:
            top_choice = st.session_state.results[0]
            st.success(f"**{t('الخيار الموصى به:', 'AI Recommendation:')}** {top_choice['name']}")
            
            st.write(t("تحليل البيانات:", "Data Analysis:"))
            
            # عرض البيانات في جدول
            df = pd.DataFrame([r['details'] for r in st.session_state.results])
            df['AI Score'] = [r['score'] for r in st.session_state.results]
            st.dataframe(df)
            
            # رسم بياني
            st.bar_chart(df.set_index('name')['AI Score'])
        else:
            st.info(t("انتظار المدخلات...", "Awaiting input..."))

elif page == t("المخزن الذكي", "Smart Inventory"):
    st.header(t("📸 الماسح الضوئي للمنتجات", "📸 Product Scanner"))
    st.write(t("استخدم الكاميرا لمسح الفاتورة أو المنتج لتحديث المخزون تلقائياً.", 
               "Use camera to scan receipts or products for auto-inventory update."))
    
    img = st.camera_input(t("التقط صورة", "Take a picture"))
    if img:
        st.success(t("تم التعرف على الصورة! جاري معالجة البيانات...", "Image captured! Processing data..."))
        # هنا يتم استدعاء كود OCR في النسخة المستقبلية

elif page == t("عن المشروع", "About Project"):
    st.header("Project Details")
    st.markdown("""
    This project is submitted as a requirement for the **Introduction to Artificial Intelligence** course at **Middle East University**.
    
    **Supervisor:**
    * Dr. Mohammed Shambour
    
    **Team Members:**
    1. Lujain Alnajar (202410697)
    2. Jude Hajjawi (202411895)
    
    **Project Description:**
    A Smart Grocery System that utilizes a weighted scoring algorithm to recommend products based on dynamic user preferences (Price, Local Support, Quality), bridging the gap between local inventory and user needs.
    """)
