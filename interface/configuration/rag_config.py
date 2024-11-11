def get_rag_config_values():
    """
    Retrieve RAG (Retrieval-Augmented Generation) configuration values.

    Returns:
    dict: A dictionary containing the RAG configuration values.
    """
    config_values = {
        'PROFILS_CHUNKS': 3500,
        'PROFILS_OVERLAP': 100,
        'PROFILS_FETCH_K': 20,
        'PROFILS_LAMBDA_MULT': 0.5,
        'PROFILS_SIMILARITY': 0.6,
        'PROFILS_DOCUMENTS': 4
    }
    with open('interface/CONFIG.py', 'r') as file:
        for line in file:
            if line.startswith('PROFILS_CHUNKS'):
                config_values['PROFILS_CHUNKS'] = int(line.split('=')[1].strip())
            elif line.startswith('PROFILS_OVERLAP'):
                config_values['PROFILS_OVERLAP'] = int(line.split('=')[1].strip())
            elif line.startswith('PROFILS_FETCH_K'):
                config_values['PROFILS_FETCH_K'] = int(line.split('=')[1].strip())
            elif line.startswith('PROFILS_LAMBDA_MULT'):
                config_values['PROFILS_LAMBDA_MULT'] = float(line.split('=')[1].strip())
            elif line.startswith('PROFILS_SIMILARITY'):
                config_values['PROFILS_SIMILARITY'] = float(line.split('=')[1].strip())
            elif line.startswith('PROFILS_DOCUMENTS'):
                config_values['PROFILS_DOCUMENTS'] = int(line.split('=')[1].strip())
    return config_values

def update_config(param_name, param_value):
    """
    Update a specific parameter in the configuration file.

    Parameters:
    param_name (str): The name of the parameter to update.
    param_value (str/int/float): The new value for the parameter.
    """
    with open('interface/CONFIG.py', 'r') as file:
        config = file.readlines()

    with open('interface/CONFIG.py', 'w') as file:
        for line in config:
            if line.startswith(param_name):
                file.write(f'{param_name} = {param_value}\n')
            else:
                file.write(line)

def rag_search_type(search_type):
    update_config('PROFILS_SEARCH_TYPE', f'"{search_type}"')

def rag_chunks(chunk_size, chunk_overlap):
    update_config('PROFILS_CHUNKS', chunk_size)
    update_config('PROFILS_OVERLAP', chunk_overlap)

def rag_fetch_k_lambda_mult(fetch_k, lambda_mult):
    update_config('PROFILS_FETCH_K', fetch_k)
    update_config('PROFILS_LAMBDA_MULT', lambda_mult)

def rag_similarity(similarity_threshold):
    update_config('PROFILS_SIMILARITY', similarity_threshold)

def rag_documents(num_documents):
    update_config('PROFILS_DOCUMENTS', num_documents)