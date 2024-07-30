import streamlit as st
from sts import recognize_from_microphone
import azure.cognitiveservices.speech as speechsdk
st.title("Speech Translator:balloon:")

if st.button("Speak"):
    st.write("Listening...")
    
    success, user_text = recognize_from_microphone()

    if success:
        st.write(f'You said:{user_text}')
        st.write('process your language')

    user_text.speech_synthesis_voice_name = "de-DE-FlorianMultilingualNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_translation_config)

    # Receives a text from console input.
    print("Type some text that you want to speak...")
    text = translation_recognition_result.translations[target_language]

    print(text)

    



    