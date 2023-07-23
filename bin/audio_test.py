import streamlit as st

audio_file = open('output.mp3','rb') #enter the filename with filepath

audio_bytes = audio_file.read() #reading the file

st.audio(audio_bytes, format='audio/ogg') #displaying the audio