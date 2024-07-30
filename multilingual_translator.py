import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
speech_key, service_region = os.environ['AZURE_SPEECH_KEY'], os.environ['SPEECH_REGION']
# speech_key = st.secrets['AZURE_SPEECH_KEY']['key']
# service_region = st.secrets['SPEECH_REGION']['region']
lang_codes = {'Arabic': 'ar-EG','Bahasa Indonesian': 'id-ID','Bengali': 'bn-IN',
            'Chinese Mandarin': 'zh-CN','Dutch': 'nl-NL','English (default)': 'en-US','French': 'fr-FR',
            'German': 'de-DE','Hindi': 'hi-IN','Italian': 'it-IT','Japanese': 'ja-JP','Korean': 'ko-KR',
            'Russian': 'ru-RU','Spanish': 'es-ES','Telugu': 'te-IN'}

with st.sidebar:
    
    lang = st.selectbox('choose your language',list(lang_codes.keys()),index = 10)
    lang_tr = st.selectbox('translate to',list(lang_codes.keys()),index = 10)

    lang_code = lang_codes[lang]
    yourlang = lang_codes[lang_tr]
    st.title("Multilingual Speech Translation")

    def recognize_from_microphone(yourlang,lang_code):
        try:
            
            # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
            speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)
            speech_translation_config.speech_recognition_language=yourlang
            target_language=lang_code
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
         
st.button("speak in"+yourlang)
if st.button("Start translation"):
        recognize_from_microphone(yourlang,lang_code)
