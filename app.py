import streamlit as st
from sts import recognize_from_microphone
st.title("Speech Translator:balloon:")

if st.button("Speak"):
    st.write("Listening...")
    success, user_text = recognize_from_microphone()

    speech_translation_config.speech_synthesis_voice_name = "de-DE-FlorianMultilingualNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_translation_config)

    # Receives a text from console input.
    print("Type some text that you want to speak...")
    text = translation_recognition_result.translations[target_language]

    print(text)

    



    