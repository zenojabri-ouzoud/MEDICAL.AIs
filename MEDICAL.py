import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

# تهيئة Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(
    page_title="الطبيب الذكي 🤖",
    page_icon="🩺",
    layout="wide"
)

# CSS للعربية
st.markdown("""
    <style>
    .stChatMessage { direction: rtl; text-align: right; }
    .main { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("🩺 الطبيب الذكي - المساعد الطبي")
st.markdown("### 🤖 تحدث معي عن أعراضك وسأساعدك")

# تهيئة تاريخ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! أنا مساعدك الطبي الذكي. أخبرني عن أعراضك وسأساعدك في التشخيص. تذكر أنني للتوعية فقط وليس بديلاً عن الطبيب."}
    ]

if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}

# عرض رسائل المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# معلومات المريض في الجانب
with st.sidebar:
    st.header("📋 معلوماتك")
    
    age = st.number_input("العمر", 0, 120, 30)
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    
    st.session_state.patient_info["age"] = age
    st.session_state.patient_info["gender"] = gender
    
    st.markdown("---")
    st.caption("⚠️ للتوعية فقط - استشر طبيباً مختصاً")
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً! كيف يمكنني مساعدتك اليوم؟ أخبرني عن أعراضك."}
        ]
        st.rerun()

# إدخال المستخدم
if prompt := st.chat_input("اكتب سؤالك أو أعراضك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # تحضير السياق
    context = f"""
    أنت طبيب ذكي متخصص في التشخيص الطبي. 
    عمر المريض: {st.session_state.patient_info.get('age', 30)}
    جنس المريض: {st.session_state.patient_info.get('gender', 'ذكر')}
    
    تاريخ المحادثة:
    {chr(10).join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])}
    
    قدم إجابة طبية مفيدة، دقيقة، وبسيطة. دائماً ذكر أن هذا ليس بديلاً عن استشارة الطبيب.
    """
    
    # الحصول على رد Gemini
    with st.chat_message("assistant"):
        with st.spinner("🔄 جاري التفكير..."):
            try:
                response = model.generate_content(context)
                reply = response.text
                
                # تحقق إذا كان طلب تشخيص
                if any(word in prompt.lower() for word in ["شخص", "تشخيص", "مرض", "أعراض"]):
                    reply += "\n\n---\n⚠️ **تنبيه:** هذا تشخيص مبدئي. استشر طبيباً مختصاً للتأكيد."
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": "عذراً، حدث خطأ. حاول مرة أخرى."})

# زر إنهاء المحادثة
if len(st.session_state.messages) > 3:
    if st.button("📋 طلب تقرير"):
        with st.spinner("جاري تحليل المحادثة..."):
            report_prompt = f"""
            بناءً على المحادثة التالية، قدم ملخصاً للتشخيص المقترح:
            {chr(10).join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])}
            
            قدم:
            1. الأعراض الرئيسية
            2. التشخيص المحتمل
            3. نصائح
            """
            try:
                report = model.generate_content(report_prompt)
                st.download_button(
                    label="📥 تحميل التقرير",
                    data=report.text,
                    file_name="تقرير_طبي.txt",
                    mime="text/plain"
                )
            except:
                st.error("خطأ في إنشاء التقرير")
