import streamlit as st
import ollama 
import json
import os
from functions.save_history import assistant_save_history
from functions.app_button import AppButton


def text_prompt(prompt, lang, model_use, session_state_updated, selected_file, history_dir, session_name):
    """
    Handle the text prompt input, process it with the language model, and manage session state.

    Parameters:
    prompt (str): The user's input prompt.
    lang (str): The language for the UI elements.
    model_use (str): The llm model to use.
    session_state_updated (list): The updated session state containing chat history.
    selected_file (str): The currently selected file name.
    history_dir (str): The directory where history files are stored.
    session_name (str): The name of the session state variable to update.

    Returns:
    list: The updated session state containing chat history.
    """
    app_btn = AppButton(lang, history_dir, selected_file, session_name)
    
    # Recover json load file if the user select and load a json
    if selected_file:
        with open(os.path.join(history_dir, selected_file), "r", encoding="utf8") as f:
            st.session_state[session_name] = json.load(f)

        app_btn.rename_file()
        app_btn.download_as_csv()
        app_btn.delete_file()

    if not selected_file:
        app_btn.new_file()

    if prompt:
        # Add user's message to message list
        session_state_updated.append({
            "role": "user",
            "content": prompt,
        })
        
        # Push the user prompt in the LLM model and return response
        with st.spinner("Réflexion.." if lang == 'fr' else "Thinking.."):
            result = ollama.chat(model=model_use, messages=session_state_updated)
            response = result["message"]["content"]
            
            # Add model response to message list
            session_state_updated.append({
                "role": "assistant",
                "content": response,
            })

        # Show all previous posts
        for message in st.session_state[session_name]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Save in new json file if first prompt or an already existing json and add updated prompt
        selected_file = assistant_save_history(session_state_updated, selected_file, history_dir, session_name)

        return session_state_updated