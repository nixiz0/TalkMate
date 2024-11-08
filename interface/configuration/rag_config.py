def get_rag_config_values():
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

def rag_search_type(search_type):
    with open('interface/CONFIG.py', 'r') as file:
        config = file.readlines()

    with open('interface/CONFIG.py', 'w') as file:
        for line in config:
            if line.startswith('PROFILS_SEARCH_TYPE'):
                file.write(f'PROFILS_SEARCH_TYPE = "{search_type}"\n')
            else:
                file.write(line)

def rag_chunks(chunk_size, chunk_overlap):
    with open('interface/CONFIG.py', 'r') as file:
        config = file.readlines()

    with open('interface/CONFIG.py', 'w') as file:
        for line in config:
            if line.startswith('PROFILS_CHUNKS'):
                file.write(f'PROFILS_CHUNKS = {chunk_size}\n')
            elif line.startswith('PROFILS_OVERLAP'):
                file.write(f'PROFILS_OVERLAP = {chunk_overlap}\n')
            else:
                file.write(line)

def rag_fetch_k_lambda_mult(fetch_k, lambda_mult):
    with open('interface/CONFIG.py', 'r') as file:
        config = file.readlines()

    with open('interface/CONFIG.py', 'w') as file:
        for line in config:
            if line.startswith('PROFILS_FETCH_K'):
                file.write(f'PROFILS_FETCH_K = {fetch_k}\n')
            elif line.startswith('PROFILS_LAMBDA_MULT'):
                file.write(f'PROFILS_LAMBDA_MULT = {lambda_mult}\n')
            else:
                file.write(line)

def rag_similarity(similarity_threshold):
    with open('interface/CONFIG.py', 'r') as file:
        config = file.readlines()

    with open('interface/CONFIG.py', 'w') as file:
        for line in config:
            if line.startswith('PROFILS_SIMILARITY'):
                file.write(f'PROFILS_SIMILARITY = {similarity_threshold}\n')
            else:
                file.write(line)

def rag_documents(num_documents):
    with open('interface/CONFIG.py', 'r') as file:
        config = file.readlines()

    with open('interface/CONFIG.py', 'w') as file:
        for line in config:
            if line.startswith('PROFILS_DOCUMENTS'):
                file.write(f'PROFILS_DOCUMENTS = {num_documents}\n')
            else:
                file.write(line)