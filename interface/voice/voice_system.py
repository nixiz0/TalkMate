import streamlit as st
import pyttsx3
import re


def split_text_and_code(text):
    """
    Split the input text into segments of text and code.

    Parameters:
    text (str): The input text containing both text and code segments.

    Returns:
    list: A list of text and code segments.
    """

    # Define a regex pattern for code detection
    pattern = r'(```.*?```)'  # This pattern matches text within triple backticks
    
    # Use regex split to separate text and code
    segments = re.split(pattern, text, flags=re.DOTALL)
    
    return segments

class NarratorVoice:
    """
    A class to handle text-to-speech functionality.

    Attributes:
    engine (pyttsx3.Engine): The text-to-speech engine.
    """

    def __init__(self):
        """
        Initialize the text-to-speech engine.
        """
        self.engine = pyttsx3.init()

    def get_voice_list(self):
        """
        Retrieve the list of available voices.

        Returns:
        dict: A dictionary of available voices with their indices as keys.
        """
        voices = self.engine.getProperty('voices')
        voice_dict = {i: voice for i, voice in enumerate(voices)}
        return voice_dict

    def select_voice(self, language):
        """
        Select a synthetic voice based on the user's language preference.

        Parameters:
        language (str): The language preference for the voice selection.

        Returns:
        str: The ID of the selected voice.
        """
        voices = self.get_voice_list()
        voice_names = [voices[i].name for i in voices]

        if 'selected_voice_id' not in st.session_state:
            st.session_state['selected_voice_id'] = voices[0].id 

        if language == "fr":
            selected_voice_name = st.sidebar.selectbox('Sélectionnez la voix synthétique à utiliser', voice_names, index=voice_names.index([voice.name for voice in voices.values() if voice.id == st.session_state['selected_voice_id']][0]))
        else:
            selected_voice_name = st.sidebar.selectbox('Select the synthetic voice to use', voice_names, index=voice_names.index([voice.name for voice in voices.values() if voice.id == st.session_state['selected_voice_id']][0]))

        st.session_state['selected_voice_id'] = [voice.id for voice in voices.values() if voice.name == selected_voice_name][0]
        return st.session_state['selected_voice_id'] 
        
    def speak(self, text):
        """
        Convert the input text to speech, skipping code segments.

        Parameters:
        text (str): The input text to be converted to speech.
        """
        # Split the text into text and code segments
        segments = split_text_and_code(text)
        
        for segment in segments:
            # Check if the segment is code
            if segment.startswith('```') and segment.endswith('```'):
                print("Code detected, not reading out loud.")
            else:
                voice = st.session_state.get('selected_voice_id', None)
                
                # Set narrator voice
                self.engine.setProperty('voice', voice)

                # Convert text to speech
                self.engine.say(segment)

                # Wait for any pending speech to complete
                self.engine.runAndWait()