import streamlit as st
import os
import re
import json
import nltk
import re
from nltk.corpus import stopwords


def assistant_save_history(session_state_updated, selected_file, history_dir, session_name):
    """
    Save the chat history to a json file and update the session state.

    Parameters:
    session_state_updated (list): The updated session state containing chat history.
    selected_file (str): The currently selected file name.
    history_dir (str): The directory where history files are stored.
    session_name (str): The name of the session state variable to update.

    Returns:
    selected_file: The name of the file where the chat history was saved.
    """

    # Check if stopwords for English and French are already downloaded
    try:
        nltk.corpus.stopwords.words('english')
        nltk.corpus.stopwords.words('french')
    except LookupError:
        nltk.download('stopwords')

    stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))

    # Create file name from user's words and clean the text
    first_user_message = session_state_updated[0]['content']
    cleaned_message = re.sub(r'\W+', ' ', first_user_message).lower()
    cleaned_message = " ".join(word for word in cleaned_message.split() if word not in stop_words)
    history_file_name = " ".join(cleaned_message.split()[:20]) + ".json"

    if 'user' in session_state_updated[0]['role'] and not selected_file:
        history_file_path = os.path.join(history_dir, history_file_name)
    else:
        history_file_path = os.path.join(history_dir, selected_file)

    # Save chat history to a file
    with open(history_file_path, "w", encoding="utf8") as f:
        json.dump(session_state_updated, f, indent=4, ensure_ascii=False)

    # Update selected file
    selected_file = history_file_name

    # Update session_name with 'session_state_updated'
    st.session_state[session_name] = session_state_updated
    st.rerun()
    return selected_file


def profil_save_history(actual_profile, history_dir, session_name):
    """
    Save the conversation history to a json file and update the session state.

    Parameters:
    actual_profile (str): The profile name of the user.
    history_dir (str): The directory where history files are stored.
    session_name (str): The name of the session state variable to update.
    """

    # Download stopwords if they are not already downloaded
    try:
        nltk.corpus.stopwords.words('english')
        nltk.corpus.stopwords.words('french')
    except LookupError:
        nltk.download('stopwords')

    # Check if the history directory exists, if not create it
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    # Create file name from user's words and clean the text
    stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))
    first_user_message = st.session_state[session_name][0]['user']
    cleaned_message = re.sub(r'\W+', ' ', first_user_message).lower()
    cleaned_message = " ".join(word for word in cleaned_message.split() if word not in stop_words)
    history_file_name = "[" + actual_profile + "]" + " " + " ".join(cleaned_message.split()[:5]) + ".json"

    # Save the conversation to a JSON file
    with open(os.path.join(history_dir, history_file_name), 'w', encoding="utf8") as f:
        json.dump(st.session_state[session_name], f, indent=4, ensure_ascii=False)