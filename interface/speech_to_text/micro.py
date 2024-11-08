import streamlit as st
import pyaudio


def get_microphone_list():
    try:
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        devices = {}
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices[i] = p.get_device_info_by_host_api_device_index(0, i).get('name')
        if not devices:
            st.warning("No microphone detected")
        return devices
    except Exception as e:
        st.error(f"An error occured {e}")
        return {}

def select_microphone(language):
    devices = get_microphone_list()
    device_names = [devices[i] for i in devices]

    if 'selected_device_index' not in st.session_state:
        st.session_state['selected_device_index'] = 0

    if language == "fr":
        selected_device_name = st.sidebar.selectbox('Sélectionnez le microphone à utiliser', device_names, index=st.session_state['selected_device_index'])
    else:
        selected_device_name = st.sidebar.selectbox('Select the microphone to use', device_names, index=st.session_state['selected_device_index'])
    st.session_state['selected_device_index'] = list(devices.values()).index(selected_device_name)

    return st.session_state['selected_device_index']
