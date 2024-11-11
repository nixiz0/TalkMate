import streamlit as st
from PIL import Image


def set_page_title(title):
    """
    Set the page title and favicon for the Streamlit application.

    Parameters:
    title (str): The title to set for the page.
    """
    favicon = Image.open('./interface/ressources/icon.png')
    st.set_page_config(
        page_title=title,
        page_icon=favicon,
    )
    st.markdown(unsafe_allow_html=True, body=f"""
        <iframe height=0 srcdoc="<script>
            parent.document.title = '{title}';
        </script>" />
    """)