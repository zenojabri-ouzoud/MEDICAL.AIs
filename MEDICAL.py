import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(
    page_title="الطبيب الذكي 🤖",
    page_icon="🩺",
    layout="wide"
)

# CSS
st.markdown("""
    <style>
    .stChatMessage { direction: rtl; text-align: right; }
    .main { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 الطبيب الذكي")

# تهيئة سريعة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً! أخبرني عن أعراضك"}
    ]

if "patient_info" not in st.session_state:
    st.session_state.patient_info = {"age": 30, "gender": "ذكر"}

# عرض الرسائل (بدون إعادة تحميل)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sidebar
with st.sidebar:
    st.header("📋 معلوماتك")
    age = st.number_input("العمر", 0, 120, 30, key="age_input")
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"], key="gender_input")
    st.session_state.patient_info["age"] = age
    st.session_state.patient_info["gender"] = gender
    
    if st.button("🗑️ مسح", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً! أخبرني عن أعراضك"}]
        st.rerun()
    
    st.caption("⚡ نسخة سريعة")

# Input
if prompt := st.chat_input("اكتب أعراضك..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # رد سريع
    with st.chat_message("assistant"):
        with st.spinner("⌛"):
            try:
                # سياق مختصر
                context = f"""
                مريض عمر {st.session_state.patient_info.get('age', 30)}، {st.session_state.patient_info.get('gender', 'ذكر')}.
                السؤال: {prompt}
                قدم تشخيصاً مختصراً ومفيداً.
                """
                
                response = model.generate_content(context)
                reply = response.text
                
                # اختصار الرد
                if len(reply) > 500:
                    reply = reply[:500] + "..."
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error("❌ خطأ")
                st.session_state.messages.append({"role": "assistant", "content": "حدث خطأ، حاول مرة أخرى"})
