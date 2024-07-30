import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
speech_key, service_region = os.environ['AZURE_SPEECH_KEY'], os.environ['SPEECH_REGION']
print(speech_key)
print(service_region)
st.title("Speech Translation")

def recognize_from_microphone():
    try:
        
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)
        speech_translation_config.speech_recognition_language="en-US"
        target_language="de"
        speech_translation_config.add_target_language(target_language)
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)
        
        st.info("Speak into your microphone 🗣️...", icon="💡")
        with st.spinner("Listening..."):
            
            translation_recognition_result = translation_recognizer.recognize_once_async().get()

            if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
                st.subheader("Translation")
                st.success("""Translated into '{}': {}""".format(
                    target_language, 
                    translation_recognition_result.translations[target_language]))
                
            elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                st.error("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
            elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = translation_recognition_result.cancellation_details
                st.error("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    st.error("Error details: {}".format(cancellation_details.error_details))
                    st.error("Did you set the speech resource key and region values?")
            speech_translation_config.speech_synthesis_voice_name = "de-DE-FlorianMultilingualNeural"

            # Creates a speech synthesizer using the default speaker as audio output.
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_translation_config)

            # Receives a text from console input.
            print("Type some text that you want to speak...")
            text = translation_recognition_result.translations[target_language]

            print(text)

            # Synthesizes the received text to speech.
            # The synthesized speech is expected to be heard on the speaker with this line executed.
            result = speech_synthesizer.speak_text_async(text).get()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
         

if st.button("Start Transcription"):
        recognize_from_microphone()
