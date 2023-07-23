import streamlit as st
import IPython.display as display

# Create the audio object.
audio = display.Audio(
    "output.mp3",
    autoplay=True,
)

# Display the audio object.
st.display(audio)
