import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')  # أسرع نموذج

model = get_model()

st.set_page_config(page_title="الطبيب الذكي", page_icon="🩺")

st.title("🩺 الطبيب الذكي ⚡")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "مرحباً! كيف يمكنني مساعدتك؟"}]

# عرض أسرع
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("اكتب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("⌛"):
            try:
                response = model.generate_content(prompt)
                reply = response.text
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except:
                st.write("❌ خطأ، حاول مرة أخرى")
