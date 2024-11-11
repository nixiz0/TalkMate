import streamlit as st
import subprocess
import tempfile
import os


def show_modelfile_llm(model_use):
    """
    Display the model file content for the specified llm.

    Parameters:
    model_use (str): The name of the model to display.

    Returns:
    tuple: A tuple containing the system text, model file content, temperature, top_k, and top_p values.
    """
    result = subprocess.run(["ollama", "show", model_use, "--modelfile"], capture_output=True, text=True, encoding='utf-8')
    output = result.stdout

    # Extract the text starting from the first "FROM"
    modelfile = ""
    in_from_section = False
    for line in output.splitlines():
        if line.strip().startswith("FROM"):
            in_from_section = True
        if in_from_section:
            modelfile += line + "\n"
    
    # If no FROM section was found, set default message
    if not modelfile:
        modelfile = "FROM \" \""
    
    # Extract the text under "SYSTEM" and stop before "PARAMETER"
    system_text = ""
    in_system_section = False
    for line in output.splitlines():
        if line.strip().startswith("SYSTEM"):
            in_system_section = True
        elif line.strip().startswith("PARAMETER"):
            in_system_section = False
        if in_system_section:
            system_text += line + "\n"
    
    # If no SYSTEM section was found, set default message
    if not system_text:
        system_text = "SYSTEM \" \""
    
    # Extract the temperature, top_k, and top_p values if they exist
    temperature = 0.7  # Default value
    top_k = 40  # Default value
    top_p = 0.90  # Default value
    for line in output.splitlines():
        if line.strip().startswith("PARAMETER temperature"):
            temperature = float(line.split()[-1])
        elif line.strip().startswith("PARAMETER top_k"):
            top_k = int(line.split()[-1])
        elif line.strip().startswith("PARAMETER top_p"):
            top_p = float(line.split()[-1])
    
    return system_text, modelfile, temperature, top_k, top_p

def rebuild_llm(model_use, modified_system_text, modelfile):
    """
    Rebuild the llm with the modified system text and model file content.

    Parameters:
    model_use (str): The name of the model to rebuild.
    modified_system_text (str): The modified system instruct to include.
    modelfile (str): The original model file content.
    """
    # Remove LICENSE section if it exists
    new_modelfile = ""
    in_license_section = False
    for line in modelfile.splitlines():
        if line.strip().startswith("LICENSE"):
            in_license_section = True
        elif in_license_section and line.strip().endswith("\""):
            in_license_section = False
            continue
        if not in_license_section:
            new_modelfile += line + "\n"
    
    # Insert the modified SYSTEM text before the first PARAMETER section
    system_inserted = False
    final_modelfile = ""
    for line in new_modelfile.splitlines():
        if line.strip().startswith("PARAMETER") and not system_inserted:
            final_modelfile += modified_system_text + "\n"
            system_inserted = True
        final_modelfile += line + "\n"
    
    if not system_inserted:
        final_modelfile += modified_system_text + "\n"

    # Create a temporary file with the modified content
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.modelfile') as temp_file:
        temp_file.write(final_modelfile)
        temp_file_path = temp_file.name
    
    # Execute the ollama create command with the temporary file
    create_command = ["ollama", "create", model_use, "--file", temp_file_path]
    subprocess.run(create_command)

    # Delete the temporary file
    os.remove(temp_file_path)
    st.rerun()