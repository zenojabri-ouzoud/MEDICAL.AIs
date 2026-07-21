import streamlit as st
import yt_dlp
import os

st.title("🎵 MP3 Downloader خاص بيك")

url = st.text_input("حط رابط اليوتيوب هنا:")

if st.button("تحويل وتحميل"):
    if url:
        try:
            # إعدادات yt-dlp للتحميل كـ MP3
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'temp_audio.%(ext)s', # كيحفظو بسمية مؤقتة
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = f"{info['title']}.mp3"
                
            # إظهار زر التحميل للمستخدم
            with open(filename, "rb") as file:
                st.download_button(
                    label="📥 حمل الأغنية دابا",
                    data=file,
                    file_name=filename,
                    mime="audio/mp3"
                )
            
            # حذف الملف بعد التحميل باش ما يتقلش السيرفر
            os.remove(filename)
            
        except Exception as e:
            st.error(f"وقع خطأ: {e}")
    else:
        st.warning("المرجو إدخال رابط صالح.")
