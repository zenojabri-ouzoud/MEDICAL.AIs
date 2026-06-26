import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# تحميل المتغيرات
load_dotenv()

# تهيئة Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام التشخيص الطبي بالذكاء الاصطناعي",
    page_icon="🏥",
    layout="wide"
)

# CSS مخصص للغة العربية
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stApp {
        font-family: 'Arial', sans-serif;
    }
    .arabic-text {
        font-size: 18px;
        line-height: 1.8;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.title("🏥 نظام التشخيص الطبي بالذكاء الاصطناعي")
st.markdown("### 🤖 مدعوم بتقنية Gemini من Google")
st.markdown("---")

# دالة تحليل الأعراض
def analyze_symptoms(symptoms_text, age, gender, medical_history):
    """تحليل الأعراض باستخدام Gemini"""
    
    prompt = f"""
    أنت طبيب مختص في التشخيص الطبي. قم بتحليل الحالة التالية:
    
    العمر: {age}
    الجنس: {gender}
    التاريخ الطبي: {medical_history}
    الأعراض: {symptoms_text}
    
    قم بتقديم تشخيص مبدئي مع:
    1. التشخيص المحتمل
    2. نسبة الثقة (من 0 إلى 100%)
    3. الأسباب المحتملة
    4. توصيات للعلاج
    5. متى يجب مراجعة الطبيب
    
    قدم الإجابة بصيغة JSON مع المفاتيح التالية:
    diagnosis, confidence, causes, recommendations, urgency
    
    استخدم اللغة العربية.
    """
    
    try:
        response = model.generate_content(prompt)
        # استخراج JSON من الرد
        response_text = response.text
        # تنظيف النص
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        result = json.loads(response_text)
        return result
    except Exception as e:
        st.error(f"❌ خطأ في التحليل: {str(e)}")
        return None

# الواجهة الجانبية
with st.sidebar:
    st.header("📋 معلومات المريض")
    
    age = st.number_input("العمر", min_value=0, max_value=120, value=30)
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    
    st.markdown("---")
    st.header("📝 التاريخ الطبي")
    medical_history = st.text_area(
        "الأمراض المزمنة أو الحساسية",
        placeholder="مثال: السكري، ضغط الدم، حساسية البنسلين..."
    )
    
    st.markdown("---")
    st.header("💊 الأدوية الحالية")
    current_meds = st.text_area(
        "الأدوية التي تتناولها حالياً",
        placeholder="اذكر الأدوية إن وجدت..."
    )

# المنطقة الرئيسية
st.subheader("🩺 أدخل الأعراض بالتفصيل")

# أعراض سريعة
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**الأعراض الشائعة**")
    fever = st.checkbox("حمى")
    cough = st.checkbox("سعال")
    headache = st.checkbox("صداع")
with col2:
    st.markdown("**الأعراض الهضمية**")
    nausea = st.checkbox("غثيان")
    diarrhea = st.checkbox("إسهال")
    pain = st.checkbox("ألم في البطن")
with col3:
    st.markdown("**أعراض أخرى**")
    fatigue = st.checkbox("تعب عام")
    breath = st.checkbox("ضيق في التنفس")
    chest = st.checkbox("ألم في الصدر")

# وصف الأعراض بالتفصيل
symptoms_description = st.text_area(
    "📝 وصف مفصل للأعراض",
    placeholder="اكتب وصفاً مفصلاً للأعراض التي تعاني منها، متى بدأت، شدتها، وأي تفاصيل أخرى مهمة...",
    height=150
)

# زر التشخيص
if st.button("🔍 تشخيص الحالة", type="primary", use_container_width=True):
    if not symptoms_description:
        st.warning("⚠️ الرجاء إدخال وصف للأعراض")
    else:
        with st.spinner("🔄 جاري تحليل الأعراض باستخدام الذكاء الاصطناعي..."):
            # تجميع الأعراض
            all_symptoms = symptoms_description
            if fever: all_symptoms += "\n- حمى"
            if cough: all_symptoms += "\n- سعال"
            if headache: all_symptoms += "\n- صداع"
            if nausea: all_symptoms += "\n- غثيان"
            if diarrhea: all_symptoms += "\n- إسهال"
            if pain: all_symptoms += "\n- ألم في البطن"
            if fatigue: all_symptoms += "\n- تعب عام"
            if breath: all_symptoms += "\n- ضيق في التنفس"
            if chest: all_symptoms += "\n- ألم في الصدر"
            
            # تحليل الأعراض
            result = analyze_symptoms(
                all_symptoms,
                age,
                gender,
                f"{medical_history} {current_meds}"
            )
            
            if result:
                # عرض النتائج
                st.markdown("---")
                st.subheader("📊 نتائج التشخيص")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"### 🏥 التشخيص المحتمل")
                    st.write(f"**{result.get('diagnosis', 'غير متوفر')}**")
                    
                    confidence = result.get('confidence', '0%')
                    st.metric("نسبة الثقة", confidence)
                
                with col2:
                    urgency = result.get('urgency', '')
                    if 'طوارئ' in urgency or 'مستعجل' in urgency:
                        st.error(f"### ⚠️ حالة مستعجلة")
                    elif 'مراجعة' in urgency:
                        st.warning(f"### 🟡 يحتاج مراجعة")
                    else:
                        st.info(f"### ℹ️ معلومات")
                    st.write(urgency)
                
                # الأسباب المحتملة
                st.markdown("### 🧬 الأسباب المحتملة")
                causes = result.get('causes', [])
                if isinstance(causes, list):
                    for cause in causes:
                        st.write(f"- {cause}")
                else:
                    st.write(causes)
                
                # التوصيات
                st.markdown("### 💊 التوصيات")
                recommendations = result.get('recommendations', [])
                if isinstance(recommendations, list):
                    for rec in recommendations:
                        st.info(f"📌 {rec}")
                else:
                    st.info(recommendations)
                
                # تحذير
                st.markdown("---")
                st.warning("""
                ⚠️ **تنبيه مهم**: 
                هذا التشخيص مقدم من الذكاء الاصطناعي لأغراض معلوماتية فقط. 
                لا يعتبر بديلاً عن استشارة الطبيب المختص. 
                في حالة الطوارئ، اتصل على رقم الطوارئ المحلي.
                """)
                
                # زر لحفظ النتائج
                if st.button("💾 حفظ النتائج"):
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_data = {
                        "timestamp": timestamp,
                        "age": age,
                        "gender": gender,
                        "symptoms": all_symptoms,
                        "diagnosis": result
                    }
                    # حفظ في session state
                    if 'history' not in st.session_state:
                        st.session_state.history = []
                    st.session_state.history.append(save_data)
                    st.success("✅ تم حفظ النتائج بنجاح!")

# عرض تاريخ التشخيص
if 'history' in st.session_state and st.session_state.history:
    with st.expander("📚 تاريخ التشخيصات السابقة"):
        for i, record in enumerate(st.session_state.history):
            st.markdown(f"**تشخيص {i+1}** - {record['timestamp']}")
            st.write(f"**التشخيص:** {record['diagnosis'].get('diagnosis', 'N/A')}")
            st.markdown("---")
