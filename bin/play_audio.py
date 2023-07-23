import streamlit as st
import google.cloud.texttospeech as tts

# Set the text to be synthesized.
text = "Hello, world!"

# Set the voice parameters.
voice = tts.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=tts.SsmlVoiceGender.NEUTRAL,
)

# Set the audio file type.
audio_config = tts.AudioConfig(
    audio_encoding=tts.AudioEncoding.MP3,
    speaking_rate=1.0
)

# Synthesize the speech.
response = tts.synthesize_speech(
    synthesis_input=tts.SynthesisInput(text=text), voice=voice, audio_config=audio_config
)

# Play the audio using Streamlit.
st.audio(response.audio_content, format="mp3")
