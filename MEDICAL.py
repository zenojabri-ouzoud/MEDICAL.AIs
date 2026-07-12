import streamlit as st
import random

# قاعدة البيانات بـ 40 دولة
data = {
    "Morocco": "Rabat", "France": "Paris", "Japan": "Tokyo", "Egypt": "Cairo",
    "Germany": "Berlin", "Italy": "Rome", "Spain": "Madrid", "UK": "London",
    "USA": "Washington", "Canada": "Ottawa", "China": "Beijing", "Russia": "Moscow",
    "Brazil": "Brasilia", "Argentina": "Buenos Aires", "Australia": "Canberra",
    "India": "New Delhi", "Turkey": "Ankara", "South Korea": "Seoul",
    "Saudi Arabia": "Riyadh", "UAE": "Abu Dhabi", "Nigeria": "Abuja",
    "South Africa": "Pretoria", "Mexico": "Mexico City", "Netherlands": "Amsterdam",
    "Belgium": "Brussels", "Switzerland": "Bern", "Sweden": "Stockholm",
    "Norway": "Oslo", "Finland": "Helsinki", "Denmark": "Copenhagen",
    "Greece": "Athens", "Portugal": "Lisbon", "Poland": "Warsaw",
    "Thailand": "Bangkok", "Vietnam": "Hanoi", "Indonesia": "Jakarta",
    "Malaysia": "Kuala Lumpur", "Iran": "Tehran", "Pakistan": "Islamabad",
    "Qatar": "Doha"
}

st.title("🎮 لعبة تخمين العاصمة")

# تهيئة السكور والأسئلة في الجلسة (Session State)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'country' not in st.session_state:
    st.session_state.country = random.choice(list(data.keys()))

country = st.session_state.country

st.write(f"### ما هي عاصمة دولة: {country}؟")
guess = st.text_input("اكتب العاصمة هنا:")

if st.button("تحقق"):
    if guess.strip().capitalize() == data[country]:
        st.success("✅ صحيح! أحسنت.")
        st.session_state.score += 1
        st.session_state.country = random.choice(list(data.keys()))
        st.rerun() # لإعادة تحميل الصفحة للسؤال الموالي
    else:
        st.error("❌ خطأ، حاول مرة أخرى!")

st.write(f"### مجموع نقاطك: {st.session_state.score}")

if st.button("إعادة اللعبة من الصفر"):
    st.session_state.score = 0
    st.session_state.country = random.choice(list(data.keys()))
    st.rerun()
