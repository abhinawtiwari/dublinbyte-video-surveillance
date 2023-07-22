import os
import pandas as pd
from google.cloud import texttospeech 
from google.cloud import texttospeech_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"
client = texttospeech_v1.TextToSpeechClient()
quote = 'The habit of saving is itself an education; it fosters every'
synthesis_input = texttospeech_v1.SynthesisInput(text=quote)
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="hi-IN", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)


audio_config = texttospeech_v1.AudioConfig(
    
    audio_encoding=texttospeech_v1.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open("output.mp3", "wb") as out:
   
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')