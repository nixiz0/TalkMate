import streamlit as st
from CONFIG import LANG
from configuration.modelfile_llm import show_modelfile_llm, rebuild_llm


def custom_llm(model_use):
    """
    Configure and update the custom language model settings.

    Parameters:
    model_use (str): The name of the model to use.
    """
    modelfile_values = {
        'system_text': "",
        'modelfile': "",
        'temperature': 0.7,
        'top_k': 40,
        'top_p': 0.90
    }

    for key, value in modelfile_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.model_use != model_use:
        st.session_state.model_use = model_use
        st.session_state.system_text, st.session_state.modelfile, st.session_state.temperature, st.session_state.top_k, st.session_state.top_p = show_modelfile_llm(model_use)
    
    # Add an input for the model name
    model_name_input = st.sidebar.text_input("Nom du modèle" if LANG == 'fr' else "Name of the model", value=st.session_state.model_use)
    
    # Display the extracted text in a text area
    modified_system_text = st.sidebar.text_area("Instruction Système" if LANG == 'fr' else "System Instruction", st.session_state.system_text, height=180, key='system_text_area')

    # Add a number input for temperature
    temperature = st.sidebar.number_input("Temperature", min_value=0.1, max_value=1.0, value=st.session_state.temperature, step=0.1)
    top_k = st.sidebar.number_input("Top_k", min_value=10, max_value=100, value=st.session_state.top_k, step=10)
    top_p = st.sidebar.number_input("Top_p", min_value=0.4, max_value=0.96, value=st.session_state.top_p, step=0.05)

    # Update the SYSTEM text with the chosen parameters
    modified_system_text += f"\nPARAMETER temperature {temperature}\n"
    modified_system_text += f"PARAMETER top_k {top_k}\n"
    modified_system_text += f"PARAMETER top_p {top_p}\n"

    # Check if the text area content has changed
    if st.sidebar.button("Créer" if LANG == 'fr' else "Create"):
        model_name = model_name_input if model_name_input else st.session_state.model_use
        rebuild_llm(model_name, modified_system_text, st.session_state.modelfile)