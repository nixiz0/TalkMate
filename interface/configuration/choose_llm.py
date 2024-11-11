import subprocess
import streamlit as st
from CONFIG import LANG


def view_install_llms():
    """
    Retrieve and display the list of ollama installed llm.

    Returns:
    list: A list of installed language model names.
    """
    try:
        # Run 'ollama list' command and get the output
        output = subprocess.check_output("ollama list", shell=True).decode()

        # Split the output into lines and ignore the first line
        lines = output.split('\n')[1:]

        # Retrieve only model names
        model_names = [line.split()[0] for line in lines if line]

        return model_names

    except subprocess.CalledProcessError as e:
        # Handle the error and display a message based on the user's language
        if LANG == 'fr':
            st.error("Veuillez démarrer votre Ollama pour accéder à vos LLMs.")
        else:
            st.error("Please start your Ollama to access your LLMs.")
        return []


def get_llm(LLM_OF_PAGE, model_name):
    """
    Set the specified language model in the configuration file.

    Parameters:
    LLM_OF_PAGE (str): The configuration variable for the language model.
    model_name (str): The name of the model to set.
    """
    try:
        with open('interface/CONFIG.py', 'r') as file:
            lines = file.readlines()
        
        with open('interface/CONFIG.py', 'w') as file:
            for line in lines:
                if line.startswith(f'{LLM_OF_PAGE} ='):
                    file.write(f"{LLM_OF_PAGE} = '{model_name}'\n")
                else:
                    file.write(line)
        st.success(f"LLM choisi : {model_name}" if LANG == 'fr' else f"LLM chosen : {model_name}")
    except Exception as e:
        st.error(f"Échec lors de la sélection du modèle : {e}" f"Failed selecting a model : {e}")
