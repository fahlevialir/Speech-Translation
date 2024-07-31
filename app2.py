import azure.cognitiveservices.speech as speechsdk
import streamlit as st

# Set up Azure Speech Service credentials
with st.sidebar:
    speech_key = st.text_input("Azure OpenAI Key", key="chatbot_api_key", type="password")
    service_region = st.text_input("region service", key="region_service", type="password")

def speech_recognize_once_from_mic():
    # Set up the speech config and audio config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)

    # Create a speech recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    st.write("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return f"Recognized: {result.text}"
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation_details.reason}"
    else:
        return "Unknown error"

# Simple UI for processing the audio input

st.title("Azure Speech Service with Streamlit")

if st.button('Start speech recognition'):
    recognition_result = speech_recognize_once_from_mic()
    st.write(recognition_result)