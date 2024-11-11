import streamlit as st
import os
import json
import pandas as pd
import base64
import string


class AppButton:
    """
    A class to handle app button in Streamlit app.
    """
    def __init__(self, lang, history_dir, selected_file, session_name=None):
        """
        Initialize the AppButton class with the given parameters.

        Parameters:
        lang (str): The language for the UI elements.
        history_dir (str): The directory where history files are stored.
        selected_file (str): The currently selected file name.
        session_name (str, optional): The name of the session state variable to update.
        """
        self.lang = lang
        self.history_dir = history_dir
        self.selected_file = selected_file
        self.session_name = session_name

    def rename_file(self):
        """
        Rename the selected file based on user input from the sidebar.
        """
        new_file_name = st.sidebar.text_input('Nouveau nom' if self.lang == 'fr' else 'New name')
        if new_file_name:
            new_file_name = new_file_name.translate(str.maketrans('', '', string.punctuation))
            if st.sidebar.button('Renommer' if self.lang == 'fr' else 'Rename'):
                if not new_file_name.endswith('.json'):
                    new_file_name += '.json'
                os.rename(os.path.join(self.history_dir, self.selected_file), os.path.join(self.history_dir, new_file_name))
                if self.session_name:
                    st.session_state[self.session_name] = []
                st.rerun()
        else:
            st.sidebar.warning('Veuillez entrer un nom de fichier.' if self.lang == 'fr' else 'Please enter a file name.')

    def delete_file(self):
        """
        Delete the selected file.
        """
        if st.sidebar.button('Supprimer' if self.lang == 'fr' else 'Delete'):
            os.remove(os.path.join(self.history_dir, self.selected_file))
            if self.session_name:
                st.session_state[self.session_name] = []
            st.rerun()

    def new_file(self):
        """
        Create a new file and update the session state.
        """
        if self.session_name and st.sidebar.button('Nouveau' if self.lang == 'fr' else 'New'):
            st.session_state[self.session_name] = []
            st.rerun()

    def download_as_csv(self):
        """
        Download the selected file as a CSV.
        """
        if st.sidebar.button('Télécharger CSV' if self.lang == 'fr' else 'Download CSV'):
            with open(os.path.join(self.history_dir, self.selected_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False, encoding='utf-8')
                b64 = base64.b64encode(csv.encode()).decode()
                csv_file_name = self.selected_file.replace('.json', '.csv')
                href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file_name}">{"Cliquez pour télécharger" if self.lang == "fr" else "Click to download"}</a>'
                st.sidebar.markdown(href, unsafe_allow_html=True)
